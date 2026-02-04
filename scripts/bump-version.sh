#!/usr/bin/env bash

# Script to manage version bumps locally
# Usage: ./scripts/bump-version.sh [patch|minor|major]

set -e

BUMP_TYPE="${1:-patch}"
VERSION_FILE="VERSION"

if [ ! -f "$VERSION_FILE" ]; then
    echo "Error: VERSION file not found"
    exit 1
fi

CURRENT_VERSION=$(cat "$VERSION_FILE")
echo "Current version: $CURRENT_VERSION"

IFS='.' read -r -a VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR="${VERSION_PARTS[0]}"
MINOR="${VERSION_PARTS[1]}"
PATCH="${VERSION_PARTS[2]}"

case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "Error: Invalid bump type. Use: patch, minor, or major"
        exit 1
        ;;
esac

NEW_VERSION="${MAJOR}.${MINOR}.${PATCH}"
echo "$NEW_VERSION" > "$VERSION_FILE"
echo "Version bumped to: $NEW_VERSION"
