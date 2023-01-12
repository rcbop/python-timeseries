import pytest
from api.filters import (InvalidFieldError, InvalidOperatorError,
                         InvalidQueryError, QueryFilters)

valid_fields = [
    "timestamp",
    "metadata",
    "metadata.area",
    "metadata.type",
    "metadata.uuid",
    "value",
    "limit",
]


@pytest.mark.parametrize("test_case,raw_query, expected", [
    (
        "complex query >>>",
        "timestamp[gte]=2022-12-28T21:29:37.448000&timestamp[lte]=2022-12-28T20:35:41.410000&limit=2&metadata.area=kitchen",
        {
            "timestamp": {
                "gte": "2022-12-28T21:29:37.448000",
                "lte": "2022-12-28T20:35:41.410000",
            },
            "limit": "2",
            "metadata.area": "kitchen"
        }
    ),
    (
        "empty values >>>",
        "timestamp[gte]=2022-12-28T21:29:37.448000&limit=2&metadata.area=",
        {
            "timestamp": {
                "gte": "2022-12-28T21:29:37.448000",
            },
            "limit": "2"
        }
    ),
    (
        "repeated values - only the first one is considered >>>",
        "timestamp[gte]=2022-12-28T21:29:37.448000&limit=2&metadata.area=kitchen&metadata.area=bedroom",
        {
            "timestamp": {
                "gte": "2022-12-28T21:29:37.448000",
            },
            "limit": "2",
            "metadata.area": "kitchen",
        }
    ),
    (
        "simple query - seconds precision >>>",
        "timestamp[lt]=2022-12-31T21:29:37",
        {
            "timestamp": {
                "lt": "2022-12-31T21:29:37",
            }
        }
    ),
    (
        "multiple empty values >>>",
        "timestamp[gte]=&limit=2&timestamp[lt]=2022-12-31T21:29:37&metadata.area=&metadata.area=",
        {
            "limit": "2",
            "timestamp": {
                "lt": "2022-12-31T21:29:37",
            }
        }
    )
])
def test_parse(test_case: str, raw_query: str, expected: dict[str, dict[str, str]]):
    """Test the parse_query_string function."""
    print(f"Test case: {test_case}")
    result = QueryFilters(
        valid_fields=valid_fields).parse_and_validate(raw_query)
    assert result == expected


@ pytest.mark.parametrize("test_case,raw_query,error_raised", [
    (
        "invalid field >>>",
        "timestamp[gte]=2022-12-28T21:29:37.448000&timestamp[lte]=2022-12-28T20:35:41.410000&limit=2&metadata.area=kitchen&invalid_field=invalid_value",
        InvalidFieldError
    ),
    (
        "invalid operator >>>",
        "timestamp[invalid_operator]=2022-12-28T21:29:37.448000&timestamp[lte]=2022-12-28T20:35:41.410000&limit=2&metadata.area=kitchen",
        InvalidQueryError
    ),
    (
        "missing value ignored >>>",
        "timestamp[gte]=2022-12-28T21:29:37.448000&timestamp[lte]=2022-12-28T20:35:41.410000&limit=2&metadata.area=",
        None
    ),
    (
        "invalid query - unbalanced brackets >>>",
        "timestamp[=&timestamp[lte]=2022-12-28T20:35:41.410000&limit=2&metadata.area=kitchen",
        InvalidQueryError
    ),
])
def test_validate(test_case: str, raw_query: str, error_raised: Exception | None):
    """Test the validate_query_string function."""
    print(f"Test case: {test_case}")
    query_filters = QueryFilters(valid_fields=valid_fields)
    if error_raised is not None:
        with pytest.raises(error_raised):
            query_filters.parse_and_validate(raw_query)
    else:
        query_filters.parse_and_validate(raw_query)
