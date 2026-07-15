#!/usr/bin/env bash
#
# git_xray.sh — dissects your repository's newest commit into Git's three
# object types (commit → tree → blob) and shows the branch pointer file,
# so lesson section 10.4 stops being a diagram and becomes something you
# have SEEN.
#
# Run it from anywhere INSIDE the repo, AFTER your first commit exists:
#   cd /mnt/d/Projects/linkboard
#   concepts/phase-00-tools-of-the-trade/playground/git_xray.sh
#
# It only READS — it changes nothing.
#
# The star of the show is `git cat-file`, Git's own microscope:
#   git cat-file -t <hash>   → what TYPE of object is this? (commit/tree/blob)
#   git cat-file -p <hash>   → pretty-print the object's content

set -euo pipefail

# Refuse to run outside a repo, with a friendly hint instead of a cryptic error.
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "[XRAY] This folder is not inside a git repository."
  echo "[XRAY] Run Part A (git init + first commit) first, then try again."
  exit 1
fi

echo "[XRAY] ================================================================"
echo "[XRAY] 1. THE COMMIT — the snapshot record"
echo "[XRAY] ================================================================"

# HEAD = "where you are now". rev-parse turns it into the actual hash.
COMMIT_HASH=$(git rev-parse HEAD)
echo "[XRAY] Your newest commit's hash (its content fingerprint):"
echo "       $COMMIT_HASH"
echo "[XRAY] Asking git what kind of object that is:  git cat-file -t"
echo "       type = $(git cat-file -t "$COMMIT_HASH")"
echo "[XRAY] And its full content:  git cat-file -p"
echo "----------------------------------------------------------------------"
git cat-file -p "$COMMIT_HASH" | sed 's/^/       /'
echo "----------------------------------------------------------------------"
echo "[XRAY] Read that: 'tree <hash>' points at the folder-listing snapshot;"
echo "[XRAY] 'parent <hash>' (if present) chains to the previous commit —"
echo "[XRAY] no parent line means this is the ROOT commit, the very first."

echo ""
echo "[XRAY] ================================================================"
echo "[XRAY] 2. THE TREE — the folder listing the commit points at"
echo "[XRAY] ================================================================"

# Extract the tree hash from the commit object we just printed.
TREE_HASH=$(git cat-file -p "$COMMIT_HASH" | awk '/^tree/ {print $2}')
echo "[XRAY] Tree $TREE_HASH contains:"
echo "----------------------------------------------------------------------"
git cat-file -p "$TREE_HASH" | sed 's/^/       /'
echo "----------------------------------------------------------------------"
echo "[XRAY] Each line: permissions, object type, hash, NAME. Notice: file"
echo "[XRAY] NAMES live here in the tree — blobs themselves are nameless"
echo "[XRAY] content. 'tree' entries are subfolders (trees inside trees)."

echo ""
echo "[XRAY] ================================================================"
echo "[XRAY] 3. A BLOB — actual file content, stored under its fingerprint"
echo "[XRAY] ================================================================"

# Grab the first blob in the root tree and show a taste of its content.
BLOB_LINE=$(git cat-file -p "$TREE_HASH" | awk '$2 == "blob"' | head -1)
BLOB_HASH=$(echo "$BLOB_LINE" | awk '{print $3}')
BLOB_NAME=$(echo "$BLOB_LINE" | awk '{print $4}')
echo "[XRAY] Taking the first blob in the root tree: '$BLOB_NAME'"
echo "[XRAY] First 10 lines of blob $BLOB_HASH:"
echo "----------------------------------------------------------------------"
git cat-file -p "$BLOB_HASH" | head -10 | sed 's/^/       /'
echo "----------------------------------------------------------------------"
echo "[XRAY] That IS your file — retrieved purely by its content hash."

echo ""
echo "[XRAY] ================================================================"
echo "[XRAY] 4. THE BRANCH — an entire 'branch' is this one tiny file:"
echo "[XRAY] ================================================================"

GIT_DIR=$(git rev-parse --git-dir)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[XRAY] File $GIT_DIR/refs/heads/$BRANCH contains exactly:"
if [[ -f "$GIT_DIR/refs/heads/$BRANCH" ]]; then
  echo "       $(cat "$GIT_DIR/refs/heads/$BRANCH")"
else
  # Newer git sometimes "packs" refs into one file instead.
  echo "       (stored in packed-refs) $(git rev-parse "$BRANCH")"
fi
echo "[XRAY] ...which is your commit's hash from step 1. A branch really is"
echo "[XRAY] just a sticky note holding one hash. Committing again will"
echo "[XRAY] simply rewrite this file to point at the new commit."
echo ""
echo "[XRAY] Done. Re-run me after ANY future commit to watch it all move."
