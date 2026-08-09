import georinex as gr
import time

print("Loading GPS only, first hour, with older xarray...")
start = time.time()

obs = gr.load(
    "data/IISC_2026_001.crx.gz",
    use="G",
    tlim=["2026-01-01T00:00:00", "2026-01-01T01:00:00"]
)

print(f"Done in {time.time() - start:.1f} seconds")
print(obs)
print("\nVariables:", list(obs.data_vars))