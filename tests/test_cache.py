import app as m
class FakeRedis:
    def __init__(self):self.data={}
    def get(self,k):return self.data.get(k)
    def setex(self,k,t,v):self.data[k]=v
    def delete(self,k):return 1 if self.data.pop(k,None) is not None else 0
    def ping(self):return True
def setup_function():
    m.redis_client=FakeRedis();m.STATS["hits"]=0;m.STATS["misses"]=0
def test_health():assert m.app.test_client().get("/health").status_code==200
def test_cache_flow():
    c=m.app.test_client();assert c.get("/api/products/1").json["source"]=="database";assert c.get("/api/products/1").json["source"]=="cache"
def test_missing():assert m.app.test_client().get("/api/products/99").status_code==404
def test_invalidate():
    c=m.app.test_client();c.get("/api/products/1");assert c.delete("/api/cache/products/1").json["removed"] is True
