#!/usr/bin/env python3
"""Local forecast bookkeeping. Python standard library only."""
import argparse, csv, hashlib, json, math, statistics, sys
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
def dt(s):
    x=datetime.fromisoformat(s.replace('Z','+00:00'))
    if x.tzinfo is None: raise ValueError('时间必须包含时区，如 +08:00')
    return x

def read(p): return json.loads(Path(p).read_text())
def save(p,x):
    with Path(p).open('x') as f: json.dump(x,f,ensure_ascii=False,indent=2)
def number(v):
    x=float(v)
    if not math.isfinite(x) or x<0: raise ValueError('数值须为有限非负数')
    return x

def integer(v):
    x=number(v)
    if not x.is_integer(): raise ValueError('播放量须为整数')
    return int(x)
def flag(v):
    if v.lower() not in ('true','false'): raise ValueError('布尔字段须为true/false')
    return v.lower()=='true'
def quantile(a,q):
    pos=(len(a)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    return a[lo]+(a[hi]-a[lo])*(pos-lo)
def validate_prediction(x):
    for key in ('point','low','high'): number(x[key])
    if not x['low']<=x['point']<=x['high']: raise ValueError('需要 low <= point <= high')
def baseline(a):
    vals=[]; ids=set(); excluded=0
    with Path(a.history).open(newline='') as f:
        for r in csv.DictReader(f):
            if r['id'] in ids: raise ValueError('历史数据ID重复')
            ids.add(r['id'])
            v=integer(r['views']); paid=flag(r['paid']); comp=flag(r['comparable'])
            if (r['platform'],r['account'],r['metric'],float(r['window_hours']))!=(a.platform,a.account,a.metric,a.window_hours) or paid or not comp:
                excluded+=1; continue
            vals.append(v)
    if len(vals)<5: raise ValueError('少于5条同口径可比样本，暂不输出数值预测')
    vals.sort()
    return dict(method='historical-quantiles-v0.1',platform=a.platform,account=a.account,metric=a.metric,window_hours=a.window_hours,n=len(vals),excluded=excluded,point=statistics.median(vals),low=quantile(vals,.1),high=quantile(vals,.9),created_at=now(),status='exploratory',history_sha256=hashlib.sha256(Path(a.history).read_bytes()).hexdigest())
def lock(a):
    b=read(a.baseline); validate_prediction(b)
    if b['n']<5 or b['window_hours']<=0: raise ValueError('无效基线')
    pred={k:b[k] for k in ('point','low','high')}; method=b['method']; reason='历史经验基线'
    if a.override:
        pred=read(a.override); validate_prediction(pred)
        reason=pred['reason']
        if not reason.strip(): raise ValueError('调整须记录依据')
        method='experimental-adjustment-v0.1'
    data=Path(a.script).read_bytes()
    out=Path(a.directory)
    out.mkdir(parents=True,exist_ok=False)
    (out/'script.snapshot.md').write_bytes(data)
    rec=dict(baseline=b,prediction=pred,method=method,reason=reason,locked_at=now(),script_sha256=hashlib.sha256(data).hexdigest(),attestation='用户确认目标未发布且未见实际结果')
    save(out/'prediction.json',rec)
    return rec

def publish(a):
    p=Path(a.directory); r=read(p/'prediction.json'); t=dt(a.at)
    if t<dt(r['locked_at']): raise ValueError('发布时间早于锁定，不能计为发布前预测')
    if t>datetime.now(timezone.utc): raise ValueError('尚未发布，不能记录未来发布')
    return write_result(p/'publication.json',dict(published_at=t.isoformat(),video_id=a.video_id,paid=a.paid))
def write_result(p,x): save(p,x); return x

def review(a):
    p=Path(a.directory); r=read(p/'prediction.json'); pub=read(p/'publication.json')
    if pub['paid']: raise ValueError('付费推广不能纳入此基线正式对账')
    if hashlib.sha256((p/'script.snapshot.md').read_bytes()).hexdigest()!=r['script_sha256']: raise ValueError('脚本快照已改变')
    at=dt(a.at); elapsed=(at-dt(pub['published_at'])).total_seconds()/3600
    if at>datetime.now(timezone.utc): raise ValueError('统计时间不能在未来')
    if elapsed<0 or abs(elapsed-r['baseline']['window_hours'])>1: raise ValueError('数据时点偏离约定窗口超过1小时')
    actual=integer(a.views); pred=r['prediction']; base=r['baseline']['point']
    x=dict(actual=actual,observed_at=at.isoformat(),elapsed_hours=elapsed,absolute_error=abs(pred['point']-actual),relative_error=None if actual==0 else abs(pred['point']-actual)/actual,hit=pred['low']<=actual<=pred['high'],interval_width=pred['high']-pred['low'],baseline_absolute_error=abs(base-actual),baseline_relative_error=None if actual==0 else abs(base-actual)/actual)
    return write_result(p/'review.json',x)
def report(a):
    groups={}; seen=set(); pending=0
    for f in sorted(Path(a.directory).rglob('prediction.json')):
        p=f.parent
        if not (p/'review.json').exists(): pending+=1; continue
        r=read(f); b=r['baseline']; x=read(p/'review.json'); pub=read(p/'publication.json')
        key=(b['platform'],b['account'],b['metric'],b['window_hours'])
        identity=(*key,pub['video_id'])
        if identity in seen: raise ValueError('同一作品有多个预测，请仅在统计目录保留主预测；其他记录移到独立档案')
        seen.add(identity); groups.setdefault(key,[]).append(x)
    result=[]
    for k,rows in groups.items():
        errors=[x['relative_error'] for x in rows if x['relative_error'] is not None]
        base=[x['baseline_relative_error'] for x in rows if x['baseline_relative_error'] is not None]
        result.append(dict(platform=k[0],account=k[1],metric=k[2],window_hours=k[3],n=len(rows),zero_actual_count=len(rows)-len(errors),mean_relative_error=statistics.mean(errors) if errors else None,baseline_mean_relative_error=statistics.mean(base) if base else None,mean_absolute_error=statistics.mean(x['absolute_error'] for x in rows),hit_rate=statistics.mean(x['hit'] for x in rows),mean_interval_width=statistics.mean(x['interval_width'] for x in rows)))
    return dict(groups=result,pending=pending,note='汇总指定目录内全部完成记录；本地记录可编辑，不是外部防篡改证明。')

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    b=sub.add_parser('baseline'); b.add_argument('history')
    for k in ('platform','account','metric'): b.add_argument('--'+k,required=True)
    b.add_argument('--window-hours',type=float,default=72)
    b.add_argument('--out',help='保存到新的JSON文件，已有文件不覆盖')
    l=sub.add_parser('lock'); l.add_argument('baseline'); l.add_argument('script'); l.add_argument('directory'); l.add_argument('--override'); l.add_argument('--unpublished-unseen',action='store_true',required=True)
    u=sub.add_parser('publish'); u.add_argument('directory'); u.add_argument('--at',required=True); u.add_argument('--video-id',required=True); u.add_argument('--paid',action='store_true')
    r=sub.add_parser('review'); r.add_argument('directory'); r.add_argument('--at',required=True); r.add_argument('--views',required=True)
    t=sub.add_parser('report'); t.add_argument('directory')
    a=p.parse_args()
    try:
        if a.cmd=='baseline' and (not math.isfinite(a.window_hours) or a.window_hours<=0): raise ValueError('时间窗口须为正数')
        value=globals()[a.cmd](a)
        if a.cmd=='baseline' and a.out: save(a.out,value)
        print(json.dumps(value,ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,TypeError) as e:
        print('错误：'+str(e),file=sys.stderr); return 2
    return 0
if __name__=='__main__': sys.exit(main())
