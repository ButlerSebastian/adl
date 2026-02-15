#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0
VIOLATIONS=0

is_snake_case() {
    local str="$1"
    if [[ -z "$str" ]]; then
        return 1
    fi
    if [[ "$str" =~ ^[a-z0-9_]+$ ]]; then
        if [[ "$str" != *_ && "$str" != _* ]]; then
            if [[ "$str" != *__* ]]; then
                return 0
            fi
        fi
    fi
    return 1
}

check_file() {
    local file="$1"
    TOTAL_FILES=$((TOTAL_FILES + 1))

    echo -n "Checking $file... "

    local violations=$(jq -r '
        def check_key(key):
            if key == null then
                ""
            elif key | test("^[a-z0-9_]+$") and key != "" and key != "_" and key != "__" and key != "_"* then
                ""
            else
                "  ❌ Invalid key: \(.key) (expected snake_case)\n"
            end;

        def check_keys(obj, prefix=""):
            if obj == null then
                ""
            elif type == "object" then
                (obj | to_entries | map(
                    check_key(prefix + .key) + check_keys(.value, prefix + .key + "_")
                ) | join(""))
            elif type == "array" then
                (obj | map(check_keys(.)) | join(""))
            else
                ""
            end;

        check_keys(.)
    ' "$file" 2>/dev/null || echo "")

    if [[ -z "$violations" ]]; then
        echo -e "${GREEN}✓${NC}"
        PASSED_FILES=$((PASSED_FILES + 1))
    else
        echo -e "${RED}✗${NC}"
        FAILED_FILES=$((FAILED_FILES + 1))
        VIOLATIONS=$((VIOLATIONS + 1))
        echo -e "${YELLOW}Violations found:${NC}"
        echo "$violations"
    fi
}

if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed${NC}"
    echo "Please install jq: sudo apt-get install jq"
    exit 1
fi

if [[ ! -d "schema" ]]; then
    echo -e "${RED}Error: schema directory not found${NC}"
    exit 1
fi

echo "Checking naming conventions in schema/ directory..."
echo "=============================================="

for file in schema/*.json; do
    if [[ -f "$file" ]]; then
        check_file "$file"
    fi
done

echo "=============================================="
echo "Summary:"
echo "  Total files checked: $TOTAL_FILES"
echo -e "  ${GREEN}Passed: $PASSED_FILES${NC}"
echo -e "  ${RED}Failed: $FAILED_FILES${NC}"
echo "  Total violations: $VIOLATIONS"

if [[ $FAILED_FILES -eq 0 ]]; then
    echo -e "\n${GREEN}✓ All files follow snake_case naming convention!${NC}"
    exit 0
else
    echo -e "\n${RED}✗ Some files do not follow snake_case naming convention${NC}"
    exit 1
fi