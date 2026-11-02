"""Validate an agent-reviewed selection ledger; never classify by keywords."""
import argparse
import json
from pathlib import Path


def check(data, reader=None, require_count=False):
    errors = []
    def need(ok, message):
        if not ok: errors.append(message)
    need(data.get('schema_version') == 1, 'schema_version must be 1')
    need(bool(data.get('criteria')), 'criteria required')
    need(bool(data.get('catalog_boundary')), 'catalog_boundary required')
    target = data.get('requested_count')
    need(type(target) is int and target > 0, 'requested_count must be positive')
    unit = data.get('count_unit')
    need(unit in ('work', 'part'), 'count_unit must be work or part')
    entries = data.get('entries', [])
    if not isinstance(entries, list): return {'errors': ['entries must be an array']}
    ids, keys, linked = set(), set(), set()
    selected, completed = 0, 0
    readings = {}
    if reader is not None:
        for item in reader.get('items', []):
            need(item.get('id') not in readings, 'duplicate reader id')
            readings[item.get('id')] = item
    for row in entries:
        label = str(row.get('id', '?'))
        need(bool(row.get('id')) and row['id'] not in ids, f'{label}: duplicate/missing id')
        ids.add(row.get('id'))
        for field in ('platform', 'work_id', 'title', 'source_url', 'reason'):
            need(bool(row.get(field)), f'{label}: {field} required')
        need(isinstance(row.get('favorite_sources'), list) and bool(row['favorite_sources']), f'{label}: favorite provenance required')
        decision = row.get('decision')
        need(decision in ('candidate', 'selected', 'excluded', 'uncertain'), f'{label}: invalid decision')
        evidence = row.get('evidence', [])
        need(isinstance(evidence, list), f'{label}: evidence must be an array')
        if not isinstance(evidence, list): evidence = []
        for ev in evidence:
            need(ev.get('kind') in ('title', 'description', 'chapter', 'transcript', 'visual') and bool(ev.get('text')) and bool(ev.get('locator')), f'{label}: incomplete evidence')
        if decision != 'selected': continue
        selected += 1
        need(any(ev.get('kind') in ('transcript', 'visual') for ev in evidence), f'{label}: selected requires body evidence')
        key = (row.get('platform'), row.get('work_id'), row.get('version', ''))
        if unit == 'part':
            need(type(row.get('part')) is int and row['part'] > 0, f'{label}: part required')
            key += (row.get('part'),)
        need(key not in keys, f'{label}: duplicate selected counting unit')
        keys.add(key)
        reader_ids = row.get('reader_ids', [])
        need(isinstance(reader_ids, list), f'{label}: reader_ids must be array')
        if not isinstance(reader_ids, list): reader_ids = []
        need(len(reader_ids) == len(set(reader_ids)), f'{label}: duplicate reader mapping')
        need(not linked.intersection(reader_ids), f'{label}: reader reused by multiple entries')
        linked.update(reader_ids)
        done = bool(reader_ids) and reader is not None
        for rid in reader_ids:
            item = readings.get(rid)
            if reader is not None:
                need(item is not None, f'{label}: missing reader {rid}')
                if item:
                    need(item.get('platform') == row.get('platform'), f'{label}: reader platform mismatch')
                    need(item.get('work_id', item.get('id')) == row.get('work_id'), f'{label}: reader work mismatch')
                    need(item.get('version', '') == row.get('version', ''), f'{label}: reader version mismatch')
                    if unit == 'part': need(item.get('part') == row.get('part'), f'{label}: reader part mismatch')
            done = done and bool(item) and item.get('status') in ('deep', 'brief')
        completed += int(done)
    if reader is not None:
        need(not (set(readings) - linked), 'reader contains items outside selected set')
    if require_count:
        need(reader is not None, '--require-count requires --reader')
        need(completed == target, f'completed {completed}, requested {target}')
    return {'selected': selected, 'completed': completed, 'requested': target,
            'shortfall': max(0, target-completed) if type(target) is int else None,
            'count_unit': unit, 'errors': errors}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--reader', type=Path)
    p.add_argument('--require-count', action='store_true')
    a = p.parse_args()
    result = check(json.loads(a.input.read_text(encoding='utf-8')),
                   json.loads(a.reader.read_text(encoding='utf-8')) if a.reader else None,
                   a.require_count)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(bool(result['errors']))
