# telepathy

Control visualizations with your ~mind~ text.

Yes I know telekenesis is the actual word for this, but telepathy sounds cooler. Can't argue with that!

**Install dependencies**

```bash
pip3 install -r requirements.text
```

## TODO

-   [x] test that umap works on dummy example
-   [x] test that supervised umap works on dummy example
-   [x] bring in image dataset
-   [x] compute the clip embeddings for the images
-   [x] given text, compute scores
-   [x] supervised umap based on the scores
-   [ ] visualize in the browser with scatter-regl or something
    -   [ ] add input to UI
    -   [ ] query the backend server with telepathy
    -   [ ] return the path, x, y, and scores to the frontend
    -   [ ] use scatter-regl to visualize the points
    -   [ ] overlap the image on hover
-   [ ] have better dependency manager
-   [ ] use NOVA to put into notebook
