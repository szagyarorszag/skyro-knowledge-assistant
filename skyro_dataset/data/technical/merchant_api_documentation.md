# Skyro Merchant API Documentation

**Version:** 2.1  
**Last Updated:** October 25, 2024  
**Base URL:** `https://api.skyro.com/v2`

## Authentication

All API requests require authentication using API keys. Include your API key in the Authorization header:

```
Authorization: Bearer sk_live_abc123xyz789
```

**API Key Types:**
- `sk_test_*` - Test mode keys for sandbox environment
- `sk_live_*` - Production keys for live transactions

**Security Best Practices:**
- Never expose API keys in client-side code
- Rotate keys every 90 days
- Use separate keys for different environments
- Revoke compromised keys immediately

---

## Core Endpoints

### 1. Create Payment

Create a new payment transaction.

**Endpoint:** `POST /payments`

**Request Body:**
```json
{
  "amount": 10000,
  "currency": "USD",
  "customer_id": "cus_abc123",
  "payment_method": "card",
  "description": "Order #12345",
  "metadata": {
    "order_id": "12345",
    "customer_email": "customer@example.com"
  },
  "capture": true
}
```

**Parameters:**
- `amount` (required, integer): Amount in smallest currency unit (cents for USD)
- `currency` (required, string): Three-letter ISO currency code (USD, EUR, GBP, etc.)
- `customer_id` (required, string): Unique customer identifier
- `payment_method` (required, string): Payment method type (card, bank_transfer, wallet)
- `description` (optional, string): Payment description for your records
- `metadata` (optional, object): Custom key-value pairs for additional data
- `capture` (optional, boolean): Whether to immediately capture payment (default: true)

**Response:**
```json
{
  "id": "pay_xyz789",
  "status": "succeeded",
  "amount": 10000,
  "currency": "USD",
  "customer_id": "cus_abc123",
  "payment_method": "card",
  "fraud_score": 15,
  "created_at": "2024-10-25T14:30:00Z",
  "captured_at": "2024-10-25T14:30:01Z"
}
```

**Status Values:**
- `pending` - Payment initiated, awaiting processing
- `processing` - Payment being processed
- `succeeded` - Payment successfully completed
- `failed` - Payment failed
- `cancelled` - Payment cancelled by merchant or customer

**Error Codes:**
- `invalid_amount` - Amount is invalid or exceeds limits
- `invalid_currency` - Currency not supported
- `insufficient_funds` - Customer has insufficient funds
- `card_declined` - Card declined by issuer
- `fraud_detected` - Transaction flagged as potentially fraudulent

---

### 2. Retrieve Payment

Get details of a specific payment.

**Endpoint:** `GET /payments/{payment_id}`

**Response:**
```json
{
  "id": "pay_xyz789",
  "status": "succeeded",
  "amount": 10000,
  "currency": "USD",
  "customer_id": "cus_abc123",
  "payment_method": "card",
  "fraud_score": 15,
  "risk_level": "low",
  "created_at": "2024-10-25T14:30:00Z",
  "captured_at": "2024-10-25T14:30:01Z",
  "refunded_amount": 0,
  "metadata": {
    "order_id": "12345"
  }
}
```

---

### 3. Refund Payment

Process a full or partial refund.

**Endpoint:** `POST /payments/{payment_id}/refunds`

**Request Body:**
```json
{
  "amount": 5000,
  "reason": "customer_request",
  "metadata": {
    "refund_reason": "Product returned"
  }
}
```

**Parameters:**
- `amount` (optional, integer): Refund amount (defaults to full payment amount)
- `reason` (required, string): Reason for refund (customer_request, duplicate, fraudulent)
- `metadata` (optional, object): Additional refund details

**Response:**
```json
{
  "id": "ref_abc456",
  "payment_id": "pay_xyz789",
  "amount": 5000,
  "currency": "USD",
  "status": "succeeded",
  "reason": "customer_request",
  "created_at": "2024-10-25T15:00:00Z"
}
```

---

### 4. List Payments

Retrieve a list of payments with optional filtering.

**Endpoint:** `GET /payments`

**Query Parameters:**
- `customer_id` (optional): Filter by customer
- `status` (optional): Filter by payment status
- `currency` (optional): Filter by currency
- `created_after` (optional): Filter payments created after timestamp
- `created_before` (optional): Filter payments created before timestamp
- `limit` (optional, default: 100): Number of results to return (max: 500)
- `page` (optional, default: 1): Page number for pagination

**Example Request:**
```
GET /payments?customer_id=cus_abc123&status=succeeded&limit=50
```

**Response:**
```json
{
  "data": [
    {
      "id": "pay_xyz789",
      "status": "succeeded",
      "amount": 10000,
      "currency": "USD",
      "created_at": "2024-10-25T14:30:00Z"
    }
  ],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 50,
    "has_more": true
  }
}
```

---

## Webhooks

Skyro sends webhook events to notify your application about payment status changes.

**Supported Events:**
- `payment.succeeded` - Payment successfully processed
- `payment.failed` - Payment failed
- `payment.refunded` - Payment refunded
- `payment.disputed` - Payment disputed by customer

**Webhook Payload:**
```json
{
  "event": "payment.succeeded",
  "timestamp": "2024-10-25T14:30:02Z",
  "data": {
    "id": "pay_xyz789",
    "status": "succeeded",
    "amount": 10000,
    "currency": "USD"
  }
}
```

**Webhook Signature Verification:**
Each webhook includes a signature in the `X-Skyro-Signature` header. Verify this signature to ensure the webhook is from Skyro:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    computed_signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)
```

---

## Rate Limits

- **Test Mode:** 100 requests per minute
- **Production Mode:** 1,000 requests per minute

Rate limit headers included in responses:
- `X-RateLimit-Limit`: Maximum requests per minute
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Timestamp when limit resets

**429 Response (Rate Limit Exceeded):**
```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests. Please retry after 60 seconds."
  }
}
```

---

## Testing

Use test mode to integrate without processing real payments.

**Test Card Numbers:**
- `4242424242424242` - Successful payment
- `4000000000000002` - Card declined
- `4000000000009995` - Insufficient funds
- `4100000000000019` - Fraud detection triggered

**Test API Key:** `sk_test_51Hxyz...`

---

## Support

- **Documentation:** https://docs.skyro.com
- **API Status:** https://status.skyro.com
- **Support Email:** api-support@skyro.com
- **Developer Slack:** Join at https://skyro.com/slack
