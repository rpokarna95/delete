#!/bin/bash
# Script to list all directories in /tmp/ and display the number of files in each

echo "=========================================="
echo "  Listing directories in /tmp/"
echo "=========================================="
echo ""

# Check if /tmp/ exists
if [ ! -d "/tmp/" ]; then
    echo "Error: /tmp/ directory does not exist!"
    exit 1
fi

# Find all directories in /tmp/ (excluding /tmp/ itself)
dirs=$(find /tmp/ -maxdepth 1 -mindepth 1 -type d 2>/dev/null)

# Check if any directories were found
if [ -z "$dirs" ]; then
    echo "No directories found in /tmp/"
    exit 0
fi

# Counter for total directories
total_dirs=0

echo "Directory Name                          | Files Present"
echo "------------------------------------------+--------------"

# Loop through each directory
while IFS= read -r dir; do
    if [ -n "$dir" ]; then
        # Get the directory name
        dir_name=$(basename "$dir")
        
        # Count files in the directory (non-recursive, files only)
        file_count=$(find "$dir" -maxdepth 1 -type f 2>/dev/null | wc -l)
        
        # Display the directory and file count
        printf "%-40s | %d\n" "$dir_name" "$file_count"
        
        ((total_dirs++))
    fi
done <<< "$dirs"

echo "------------------------------------------+--------------"
echo ""
echo "Total directories found: $total_dirs"
echo "=========================================="
