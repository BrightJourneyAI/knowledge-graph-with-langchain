# Use AI to Generate Knowledge Graphs with LangChain & Neo4j
This following code supports this article written on [Generating Knowledge Graphs using AI](https://localhost.com)

Have you ever had to work with messy, unstructured data and wished there was a way to represent it more naturally? The complexities of the world are more more like a graph than strict relational tables stored in a database. Knowledge graphs are one solution to this problem but they have one major pain, they model the world and the world is not simple to model!!! 

This example takes the transcript from multiple YouTube videos on Garmin Sports Watches and converts them into the following graph, automatically. 
<p align="center">
  <img src="images\garmin-features-graph.png?raw=true" alt="drawing" width="500"/>
</p>


## Getting Started
You'll need to add your own OpenAI key to use the repo. 


For the full breakdown of setting up all the dependencies (including a local Neo4j server on Docker) and more about knowledge graphs be sure to check out the article [here](https://localhost.com). 

This repo uses [Poetry](https://python-poetry.org/) for dependency management. 


``` 
poetry install
poetry run build_kg
```

You can change the YouTube videos easily by changing the following array to IDs of your choice. 
```
video_ids = [
            "wYJfVczBORQ", 
            "H-lDmNcKZtI", 
            "YGXNYjL1t00",
            "sY0iHU71k-4",
            "BZ1k_bvupVc"
            ]
```

After the script has completed, head on over to your Neo4j instance and inspect your brand new graph database. Enjoy. 

## Liked This?
If you liked this consider supporting me for free by [joining my twice weekly newsletter](https://bit.ly/45lG2pR) on all things AI or by treating me to a cup of coffee, if you think I deserve it. 

<a href="https://buymeacoffee.com/brightjourneyai" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>



