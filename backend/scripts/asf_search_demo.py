import asf_search as asf
import pprint

print("Starting ASF Search for Jorf Lasfar...")
opts=asf.ASFSearchOptions(**{
    "maxResults": 3, # Just 3 results to show the format
    "bbox": [
        -8.648311333381708,
        33.07701081241338,
        -8.551239363088094,
        33.145440928984286
    ],
    "dataset": [
        "SENTINEL-1"
    ]
})

results=asf.search(opts=opts)
print(f"Found {len(results)} scenes.")
if len(results) > 0:
    print("Example result:")
    pprint.pp(results[0].properties)
