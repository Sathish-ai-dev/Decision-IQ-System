# API Guidelines

## Purpose
Defines standards for all backend APIs.

## Principles
- RESTful design
- Version APIs under `/api/v1`
- JSON request/response
- Stateless services
- JWT authentication
- Role-based authorization

## Standard Response
```json
{
  "success": true,
  "message": "Operation completed.",
  "data": {},
  "meta": {}
}
```

## Error Response
```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": []
}
```

## Standards
- Pagination
- Filtering
- Sorting
- OpenAPI documentation
- Consistent HTTP status codes
- Request validation with Pydantic
