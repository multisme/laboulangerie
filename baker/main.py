import sys
from time import time

from typing import Optional

from fastapi import FastAPI, Request
from loguru import logger
from pytezos import pytezos

app = FastAPI()

client = pytezos.using(
    shell="http://localhost:20000",
    key="edpkvGfYw3LyB1UcCahKQk4rF2tvbMUk8GFiTuMjL75uGXrpvKXhjn"
)

logger.add("tests/file_{time}.log", level='DEBUG')
logger.add(sys.stderr, level="DEBUG")
logger.add(sys.stdout, level="DEBUG")
logger = logger.opt(colors=True)

keys = {
    'tz1MT1ZfNoDXzWvUj4zJg8cVq7tt7a6QcC58': 'edsk3Q3uoz73R7a2GoKHncLZMGD14rKydkiypCvrN3iXk3Ufmx6ZtR',
    'tz1ZrWi7V8tu3tVepAQVAEt8jgLz4VVEEf7m': 'edsk4QvnUzAQ3s8jiFdmpAztGtXkUoKiKJdKS4QeqdM9aZNE53q8FD',
    'tz1PMqV7qGgWMNH2HR9inWjSvf3NwtHg7Xg4': 'edsk3aE3Faxgb2mvjHGSHDW4U9TwrGnuRuamJBCcr1wbqMjR2QtXCV',
    'tz1VWU45MQ7nxu5PGgWxgDePemev6bUDNGZ2': 'edsk2sRikkzrGKnRC28UhvJsKAM19vuv4LtCRViyjkm2jMyAxiCMuG',
    'tz1azKk3gBJRjW11JAh8J1CBP1tF2NUu5yJ3': 'edsk4FxpsXkEmFG7fKygaWYJ4hb65vuH55ehM2856xAvipztVWuxJM',
    'tz1VSUr8wwNhLAzempoch5d6hLRiTh8Cjcjb': 'edsk3QoqBuvdamxouPhin7swCvkQNgq4jP5KZPbwWNnwdZpSpJiEbq',
    'tz1YPSCGWXwBdTncK2aCctSZAXWvGsGwVJqU': 'edsk3RFgDiCt7tWB2oe96w1eRw72iYiiqZPLu9nnEY23MYRp2d8Kkx',
    'tz1Vb3PvQAHTgyp56rXqSpkcaUc5zdEcFfbD': 'edsk3crF2KCjXWjPUpTSzLFkfywmiyQ3ZLaYhq1FKHTnMcZQ8fr41m',
    'tz1Q3eT3kwr1hfvK49HK8YqPadNXzxdxnE7u': 'edsk4MmZRWF3uzMLh28g4ocxHsJPzLNrKeGTwM5uX3sFDn63GMPiog',
    'tz1iPFr4obPeSzknBPud8uWXZC7j5gKoah8d': 'edsk36su9hdbfCCpJnDdCsQVs4JSbf7DcmPbeRBhpZznzEcX5gPRpP'
}


def endorse():
    endorsing_rights = client.shell.blocks['head'].helpers.endorsing_rights()
    logger.error(f"{endorsing_rights}")
    endorser_key_hash = sorted(endorsing_rights, key=lambda endorser: endorser['slots'])[0]['delegate']
    level = client.shell.blocks['head'].header.shell()['level']
    timestamp = int(time())
    operation = client.using(
        key=keys[endorser_key_hash]
    ).endorsement(level).fill(
        ttl=60, timestamp=timestamp
    ).sign().with_slot()
    logger.error(f"{operation}")
    res = operation.inject()
    logger.error(f"block {res} endorsed by {endorser_key_hash}")


def bake():
    baking_rights = client.shell.blocks['head'].helpers.baking_rights()
    logger.error(f"{baking_rights}")
    baker_key_hash = sorted(baking_rights, key=lambda baker: baker['priority'])[0]['delegate']
    timestamp = int(time())
    operation = client.using(
        key=keys[baker_key_hash]
    )
    logger.error(timestamp)
    logger.error(client.shell.blocks['head'].helpers.baking_rights())
    operation = operation.bake_block()
    operation= operation.fill(
        timestamp=timestamp
    )
    operation = operation.work()
    operation = operation.sign()
    logger.error(f"{operation}")
    res = operation.inject()
    logger.error(f"block {res} baked by {baker_key_hash}")


@app.get("/mirror")
def root(request: Request):
    logger.error("baker get was received")
    return


@app.post("/mirror")
def auto_bake():
    logger.error("baker post was received")
    endorse()
    bake()


@app.get('/')
def catch_all():
    logger.error('all catch all')
    return "hey"
