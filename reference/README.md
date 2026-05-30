# reference

`MANIFEST.yml` here is a vendored snapshot of the canonical manifest in the
upstream repository `nickjoven/harmonics`. The drawings in this repository pull
their quantitative values from that manifest, so this snapshot records the exact
version they were drawn against.

The workflow `.github/workflows/manifest-watch.yml` fetches the live upstream
manifest on a schedule and compares it to this snapshot. When the two differ it
opens an issue with the diff, which is the signal that the values behind the
plots may have moved and the affected drawings should be checked.

When the drawings have been brought back into line with a new upstream version,
refresh this snapshot so the watcher goes quiet again:

    gh api repos/nickjoven/harmonics/contents/MANIFEST.yml \
      -H "Accept: application/vnd.github.raw" > reference/MANIFEST.yml

Then commit the updated snapshot.
