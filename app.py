import json,os
import redis
from flask import Flask,jsonify

app=Flask(__name__)
redis_client=redis.Redis.from_url(os.getenv("REDIS_URL","redis://localhost:6379/0"),decode_responses=True)
CACHE_PREFIX="product:"
CACHE_TTL=60
DATABASE={"1":{"id":1,"name":"Laptop","price":65000},"2":{"id":2,"name":"Keyboard","price":1800},"3":{"id":3,"name":"Mouse","price":900}}
STATS={"hits":0,"misses":0}

def key(pid): return CACHE_PREFIX+pid

@app.get("/health")
def health():
    try:
        redis_client.ping();return jsonify({"status":"ok","redis":"connected"})
    except redis.RedisError:
        return jsonify({"status":"degraded"}),503

@app.get("/api/products/<pid>")
def get_product(pid):
    cached=redis_client.get(key(pid))
    if cached:
        STATS["hits"]+=1
        return jsonify({"source":"cache","product":json.loads(cached),"stats":STATS})
    product=DATABASE.get(pid)
    if not product:return jsonify({"error":"product_not_found"}),404
    STATS["misses"]+=1
    redis_client.setex(key(pid),CACHE_TTL,json.dumps(product))
    return jsonify({"source":"database","product":product,"stats":STATS})

@app.delete("/api/cache/products/<pid>")
def invalidate(pid):
    return jsonify({"removed":bool(redis_client.delete(key(pid))),"product_id":pid})

@app.errorhandler(404)
def nf(_):return jsonify({"error":"resource_not_found"}),404

if __name__=="__main__":app.run(host="0.0.0.0",port=5000,debug=True)
