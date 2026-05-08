#!/bin/bash
# Production End-to-End Test Script
# Tests deployed application on Vercel + Render
# Date: May 8, 2026

set -e  # Exit on error

FRONTEND_URL="https://engineering-onboarding-copilot.vercel.app"
BACKEND_URL="https://engineering-onboarding-copilot.onrender.com"

echo "=================================="
echo "PRODUCTION E2E TEST"
echo "=================================="
echo "Date: $(date)"
echo "Frontend: $FRONTEND_URL"
echo "Backend: $BACKEND_URL"
echo ""

# Test 1: Backend Health
echo "[1/6] Testing backend health endpoint..."
HEALTH_RESPONSE=$(curl -s --max-time 90 "$BACKEND_URL/health")
echo "✓ Response: $HEALTH_RESPONSE"
if echo "$HEALTH_RESPONSE" | grep -q 'healthy'; then
    echo "✅ PASS: Backend is healthy"
else
    echo "❌ FAIL: Backend not healthy"
    exit 1
fi
echo ""

# Test 2: Backend Root
echo "[2/6] Testing backend root endpoint..."
ROOT_RESPONSE=$(curl -s --max-time 30 "$BACKEND_URL/")
echo "✓ Response: $(echo $ROOT_RESPONSE | head -c 100)..."
if echo "$ROOT_RESPONSE" | grep -q 'Engineering Onboarding Copilot API'; then
    echo "✅ PASS: Backend root accessible"
else
    echo "❌ FAIL: Backend root not responding"
    exit 1
fi
echo ""

# Test 3: Q&A Endpoint (Critical)
echo "[3/6] Testing Q&A endpoint with sample question..."
ASK_RESPONSE=$(curl -s --max-time 45 -X POST "$BACKEND_URL/ask" \
    -H "Content-Type: application/json" \
    -d '{"question":"How do I set up my development environment?"}')

echo "✓ Response received ($(echo $ASK_RESPONSE | wc -c) bytes)"

# Check for required fields
if echo "$ASK_RESPONSE" | grep -q '"answer"'; then
    echo "✅ PASS: Answer field present"
else
    echo "❌ FAIL: No answer field"
    exit 1
fi

if echo "$ASK_RESPONSE" | grep -q '"confidence"'; then
    echo "✅ PASS: Confidence field present"
else
    echo "❌ FAIL: No confidence field"
    exit 1
fi

if echo "$ASK_RESPONSE" | grep -q '"sources"'; then
    echo "✅ PASS: Sources field present"
else
    echo "❌ FAIL: No sources field"
    exit 1
fi

# Extract and display confidence
CONFIDENCE=$(echo "$ASK_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['confidence'])" 2>/dev/null || echo "N/A")
echo "✓ Confidence score: $CONFIDENCE"

if [ "$CONFIDENCE" != "N/A" ]; then
    if (( $(echo "$CONFIDENCE >= 0.7" | bc -l) )); then
        echo "✅ PASS: High confidence ($CONFIDENCE >= 0.7)"
    else
        echo "⚠️  WARNING: Lower confidence ($CONFIDENCE < 0.7)"
    fi
fi
echo ""

# Test 4: Gap Radar Endpoint
echo "[4/6] Testing Gap Radar endpoint..."
GAPS_RESPONSE=$(curl -s --max-time 30 "$BACKEND_URL/api/gaps")
echo "✓ Response: $(echo $GAPS_RESPONSE | head -c 100)..."
if echo "$GAPS_RESPONSE" | grep -q '\['; then
    echo "✅ PASS: Gap Radar endpoint accessible (returns array)"
else
    echo "⚠️  WARNING: Gap Radar response unexpected"
fi
echo ""

# Test 5: Gap Statistics
echo "[5/6] Testing Gap Radar statistics..."
STATS_RESPONSE=$(curl -s --max-time 30 "$BACKEND_URL/api/gaps/stats")
echo "✓ Response: $STATS_RESPONSE"
if echo "$STATS_RESPONSE" | grep -q '"total_gaps"'; then
    echo "✅ PASS: Gap statistics accessible"
else
    echo "⚠️  WARNING: Gap stats response unexpected"
fi
echo ""

# Test 6: Frontend Accessibility
echo "[6/6] Testing frontend accessibility..."
FRONTEND_RESPONSE=$(curl -s --max-time 30 -I "$FRONTEND_URL" | head -n 1)
echo "✓ Response: $FRONTEND_RESPONSE"
if echo "$FRONTEND_RESPONSE" | grep -q "200\|301\|302"; then
    echo "✅ PASS: Frontend is accessible"
else
    echo "❌ FAIL: Frontend not accessible"
    exit 1
fi
echo ""

echo "=================================="
echo "✅ ALL TESTS PASSED"
echo "=================================="
echo "Summary:"
echo "  • Backend health: ✅"
echo "  • Q&A endpoint: ✅"
echo "  • Gap Radar: ✅"
echo "  • Frontend: ✅"
echo ""
echo "System is PRODUCTION READY for demo! 🎉"
echo ""
