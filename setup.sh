#!/bin/bash

# In case that `REPO DESCRIPTION` doesn't contain one of the cases insensitive choices.
# Choices are: react, django, phoenix, and fastapi.
export SELECTED_FRAMEWORK_NAME=$(echo "react|django|phoenix|fastapi" | grep -E -i -o -w "$REPO_DESCRIPTION")
export SELECTED_APP=$([[ -z "$SELECTED_FRAMEWORK_NAME" ]] && echo "django" || echo "$SELECTED_FRAMEWORK_NAME")
export BASHED_REPO_NAME=$(echo $REPO_NAME | tr "[:lower:]-" "[:upper:]_")
export PYTHONED_REPO_NAME=$(echo $REPO_NAME | tr "-" "_")
export CLASSIFIED_REPO_NAME=$(echo $REPO_NAME | sed -r "s/^(.)|-(.)/\U\1\2\E/g")

# Check that environment variables were correctly set.
echo "REPO_DESCRIPTION: $REPO_DESCRIPTION"
echo "REPO_NAME: $REPO_NAME"
echo "SELECTED_APP: $SELECTED_APP"
echo "SELECTED_FRAMEWORK_NAME: $SELECTED_FRAMEWORK_NAME"
echo "BASHED_REPO_NAME: $BASHED_REPO_NAME"
echo "PYTHONED_REPO_NAME: $PYTHONED_REPO_NAME"
echo "CLASSIFIED_REPO_NAME: $CLASSIFIED_REPO_NAME"

# Temp directory to keep selected-app files.
mv ./templates/$SELECTED_APP-app ./selected-app

# Remove unecessary files from `cookier-cutter` project.
find ./ -maxdepth 1 -regextype posix-extended  -not -regex "./.git|./|./selected-app" -exec rm -fr {} +
# Move to relevant files to the root
mv ./selected-app/{*,.[^.]*} ./
rm -fr ./selected-app

# Substituting variables in the selected project.
find ./ -type f -exec sed -i "s/<REPO_NAME>/$REPO_NAME/g" {} +
find ./ -type f -exec sed -i "s/<REPO_DESCRIPTION>/$REPO_DESCRIPTION/g" {} +
find ./ -type f -exec sed -i "s/<BASHED_REPO_NAME>/$BASHED_REPO_NAME/g" {} +
find ./ -type f -exec sed -i "s/<PYTHONED_REPO_NAME>/$PYTHONED_REPO_NAME/g" {} +
find ./ -type f -exec sed -i "s/<CLASSIFIED_REPO_NAME>/$CLASSIFIED_REPO_NAME/g" {} +

# Rename files per variables
find . -name '*<REPO_NAME>*' -exec bash -c ' mv $0 ${0/<REPO_NAME>/$REPO_NAME}' {} \;
