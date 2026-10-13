"""Durable independent training and checkpoint-evaluation queues."""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def connect():
    db = sqlite3.connect(ROOT/'jobs/queue.db', timeout=30)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL')
    db.executescript('''
    CREATE TABLE IF NOT EXISTS jobs (
      id INTEGER PRIMARY KEY, kind TEXT NOT NULL,
      benchmark TEXT NOT NULL, task TEXT NOT NULL, method TEXT NOT NULL,
      seed INTEGER NOT NULL, checkpoint_step INTEGER NOT NULL DEFAULT -1,
      status TEXT NOT NULL DEFAULT 'queued', prerequisite TEXT,
      config_path TEXT, checkpoint_path TEXT, pid INTEGER,
      attempts INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL DEFAULT 2,
      started TEXT, finished TEXT, exit_code INTEGER, error TEXT,
      UNIQUE(kind, benchmark, task, method, seed, checkpoint_step)
    );
    CREATE VIEW IF NOT EXISTS train_jobs AS SELECT * FROM jobs WHERE kind='train';
    CREATE VIEW IF NOT EXISTS eval_jobs AS SELECT * FROM jobs WHERE kind='eval';
    ''')
    return db

def initialize():
    protocol=json.loads((ROOT/'configs/protocol.json').read_text())
    db=connect()
    for task in protocol['tasks']:
        methods=['e0','e1','e3','e4','e6','dp_transformer','act','bc_rnn','dp3']
        if task['task'] in ['threading_d2','StackCube-v1','PegInsertionSide-v1']:
            methods += ['e2','e5','e7']
        for method in methods:
            for seed in task['seeds']:
                name=f"{task['benchmark']}/{task['task']}/{method}/seed_{seed}"
                cfg=ROOT/'configs/runs'/f'{name}.json'
                db.execute('INSERT OR IGNORE INTO jobs(kind,benchmark,task,method,seed,prerequisite,config_path) VALUES(?,?,?,?,?,?,?)',
                    ('train',task['benchmark'],task['task'],method,seed,
                     'dataset manifest + implementation + matching runner',str(cfg)))
    db.commit()
    print('registered',db.execute('SELECT count(*) FROM train_jobs').fetchone()[0],'unique main/core/extended training jobs')
    db.close()

if __name__=='__main__': initialize()
