# Redis Persistence - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Redis Dependency

```bash
# If not using Docker (local development)
pip install redis>=5.0.0
```

### Step 2: Start Redis

**Option A: Using Docker Compose (Recommended)**
```bash
cd /path/to/project
docker-compose up redis -d
```

**Option B: Local Redis**
```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Verify Redis is running
redis-cli ping  # Should output: PONG
```

### Step 3: Enable Redis Persistence

**Option A: Environment Variable**
```bash
export ENABLE_REDIS_PERSISTENCE=true
export REDIS_URL=redis://localhost:6379/0
```

**Option B: .env File**
```bash
# Create/edit .env file
echo "ENABLE_REDIS_PERSISTENCE=true" >> .env
echo "REDIS_URL=redis://localhost:6379/0" >> .env
```

**Option C: Docker Compose (Already Configured)**
```bash
# docker-compose.yml already has ENABLE_REDIS_PERSISTENCE=true
docker-compose up
```

### Step 4: Verify It's Working

```bash
# Start the application
python -m uvicorn backend.app.main:app --reload

# Check logs for confirmation
# Should see: "Using Redis repository for process storage"
# (or similar message)

# Test persistence
curl -X POST http://localhost:8001/decisions/start \
  -H "Content-Type: application/json" \
  -d '{"decision_query": "Should I learn Redis?"}'

# Copy the process_id from response

# Restart the application
# Ctrl+C, then restart

# Check status (should still exist)
curl http://localhost:8001/decisions/status/{process_id}
# Should return process info, not 404!
```

---

## 🔍 How to Check Which Repository is Being Used

### Method 1: Check Logs

```bash
# Look for startup messages
tail -f app.log | grep -i redis

# You should see:
# "Using RedisProcessRepository for process storage"
# or
# "Using InMemoryProcessRepository (Redis disabled)"
```

### Method 2: Test Persistence

```bash
# Create a process
PROCESS_ID=$(curl -X POST http://localhost:8001/decisions/start \
  -H "Content-Type: application/json" \
  -d '{"decision_query": "test"}' | jq -r '.process_id')

# Restart application

# Try to get process
curl http://localhost:8001/decisions/status/$PROCESS_ID

# If 200 OK → Redis is working ✅
# If 404 Not Found → Using in-memory ❌
```

### Method 3: Check Redis Directly

```bash
# Connect to Redis
redis-cli

# List all keys
127.0.0.1:6379> KEYS process:*

# Should see keys like:
# 1) "process:abc123"
# 2) "process:def456"

# View process data
127.0.0.1:6379> HGETALL process:abc123
```

---

## 📊 Quick Commands

### View All Processes

```bash
curl http://localhost:8001/decisions/processes
```

### Cleanup Old Processes

```bash
curl -X DELETE http://localhost:8001/decisions/cleanup
```

### Check Redis Stats

```bash
redis-cli INFO stats
redis-cli DBSIZE  # Number of keys
redis-cli INFO memory  # Memory usage
```

### Clear All Redis Data (DANGER!)

```bash
# ⚠️ This deletes EVERYTHING in the database
redis-cli FLUSHDB

# ⚠️ This deletes EVERYTHING in ALL databases
redis-cli FLUSHALL
```

---

## 🐛 Quick Troubleshooting

### "Connection refused"

```bash
# Check if Redis is running
redis-cli ping

# If not running:
# Docker: docker-compose up redis
# Local: brew services start redis (macOS) or systemctl start redis (Linux)
```

### "Process not found after restart"

```bash
# Check environment variables
env | grep REDIS

# Should see:
# ENABLE_REDIS_PERSISTENCE=true
# REDIS_URL=redis://localhost:6379/0

# If not set, Redis persistence is disabled
export ENABLE_REDIS_PERSISTENCE=true
```

### "Memory keeps growing"

```bash
# Check number of processes
redis-cli DBSIZE

# If very large, run cleanup
curl -X DELETE http://localhost:8001/decisions/cleanup

# Consider setting up automatic cleanup (see REDIS_PERSISTENCE.md)
```

---

## ⚙️ Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_REDIS_PERSISTENCE` | `false` | Enable Redis storage |
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_DB` | `0` | Redis database number (0-15) |
| `REDIS_PASSWORD` | `None` | Redis password (if required) |
| `REDIS_URL` | `None` | Full Redis URL (overrides individual settings) |

### Redis URL Format

```bash
# Without password
redis://localhost:6379/0

# With password
redis://:password@localhost:6379/0

# With username and password (Redis 6+)
redis://username:password@localhost:6379/0

# Redis Sentinel
redis-sentinel://localhost:26379/mymaster/0

# Unix socket
unix:///var/run/redis/redis.sock?db=0
```

---

## 🎯 Common Use Cases

### Use Case 1: Development (No Redis)

```bash
# Don't enable Redis (use in-memory)
export ENABLE_REDIS_PERSISTENCE=false

# Fast startup, no external dependencies
python -m uvicorn backend.app.main:app --reload
```

### Use Case 2: Development (With Redis)

```bash
# Start Redis in background
docker-compose up redis -d

# Enable Redis
export ENABLE_REDIS_PERSISTENCE=true

# Start app
python -m uvicorn backend.app.main:app --reload
```

### Use Case 3: Production (Docker Compose)

```bash
# Everything configured in docker-compose.yml
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

### Use Case 4: Production (Kubernetes)

```yaml
# kubernetes/deployment.yaml
env:
  - name: ENABLE_REDIS_PERSISTENCE
    value: "true"
  - name: REDIS_URL
    value: "redis://redis-service:6379/0"
```

---

## 📈 Performance Tips

### 1. Use Redis Database Numbers

```bash
# Separate databases for different environments
# Dev: database 0
export REDIS_DB=0

# Test: database 1
export REDIS_DB=1

# Staging: database 2
export REDIS_DB=2

# Production: separate Redis instance
```

### 2. Monitor Memory Usage

```bash
# Check current memory
redis-cli INFO memory | grep used_memory_human

# Set memory limit (in docker-compose.yml)
command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

### 3. Regular Cleanup

```bash
# Setup cron job
crontab -e

# Add line to cleanup every hour
0 * * * * curl -X DELETE http://localhost:8001/decisions/cleanup
```

---

## 🔐 Security Considerations

### 1. Use Password Protection

```bash
# In docker-compose.yml
command: redis-server --requirepass mypassword

# In environment
export REDIS_PASSWORD=mypassword
```

### 2. Bind to Localhost Only

```bash
# In docker-compose.yml
command: redis-server --bind 127.0.0.1

# Don't expose Redis port publicly
```

### 3. Use Redis ACLs (Redis 6+)

```bash
# Create user with limited permissions
redis-cli ACL SETUSER worker on >password ~process:* +get +set +del
```

---

## 📚 Next Steps

1. **Read Full Documentation**: `docs/REDIS_PERSISTENCE.md`
2. **Understand Architecture**: `docs/PHASE_7_SUMMARY.md`
3. **Set Up Monitoring**: Track Redis metrics
4. **Configure Cleanup**: Automated periodic cleanup
5. **Write Tests**: Unit and integration tests

---

## 💡 Pro Tips

1. **Use Different Redis Databases**
   - Dev: `REDIS_DB=0`
   - Test: `REDIS_DB=1`
   - Easy isolation, no conflicts

2. **Monitor Key Count**
   ```bash
   watch -n 5 'redis-cli DBSIZE'
   ```

3. **Inspect Process Data**
   ```bash
   redis-cli HGETALL process:abc123
   ```

4. **Backup Redis Data**
   ```bash
   redis-cli SAVE  # Create dump.rdb
   cp /var/lib/redis/dump.rdb ~/backup/
   ```

5. **Test Redis Failure**
   ```bash
   # Stop Redis
   docker-compose stop redis
   
   # App should fall back to in-memory
   # Check logs for "Using InMemoryProcessRepository"
   
   # Start Redis again
   docker-compose start redis
   ```

---

## ✅ Success Checklist

- [ ] Redis installed and running
- [ ] `ENABLE_REDIS_PERSISTENCE=true` set
- [ ] Application starts without errors
- [ ] Process persists after restart
- [ ] Can view processes in Redis CLI
- [ ] Cleanup endpoint works
- [ ] Monitoring set up (optional)
- [ ] Automatic cleanup configured (optional)

---

## 🆘 Need Help?

1. **Check logs**: Look for Redis connection errors
2. **Test Redis**: `redis-cli ping`
3. **Check config**: `env | grep REDIS`
4. **Read docs**: `docs/REDIS_PERSISTENCE.md`
5. **Test fallback**: Disable Redis, should use in-memory

---

**You're ready to go! 🚀**

Start with Docker Compose for the easiest experience:
```bash
docker-compose up
```

Then visit: http://localhost:8001/docs
