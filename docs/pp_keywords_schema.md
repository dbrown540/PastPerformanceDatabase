# PP_Keywords.json Schema Documentation

The PP_Keywords.json file is the state file that tracks the current state of document processing.

## Schema

```json
{
  "last_master_hash": "abc123def456",
  "last_full_success_date": "2025-03-17T14:30:00Z",
  "documents": {
    "document1.xlsx": {
      "last_successful_update": "2025-03-17T14:30:00Z",
      "current_hash": "789ghi101112",
      "status": "success",
      "attempt_count": 0
    },
    "document2.xlsx": {
      "last_successful_update": "2025-03-15T09:20:00Z",
      "current_hash": "jkl131415mno",
      "status": "locked",
      "attempt_count": 2,
      "next_attempt": "2025-03-19T12:00:00Z"
    }
  }
}