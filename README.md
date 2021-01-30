# GIMP-Background-Remover
A small plugin to easily remove the Background of a Image with [LDF](https://arxiv.org/pdf/2008.11048.pdf).  [Github of LDF](https://github.com/weijun88/LDF). 

## THIS WORKS ONLY FOR GIMP 3
Currently in development

## Installation:

### Linux: 
1. Install python

2. Put the background-remover folder in your Gimp Plugins directory

3. make the python file executable and install dependecies with: 

```
bash setup.sh
```

4. Download the model and weights and put both in the Ldf directory:

    [Trained Model](https://drive.google.com/file/d/1qGQ6wSWTFqt8oy_YT3_aj-_pdlf5vKWL/view?usp=sharing)

    [model](https://download.pytorch.org/models/resnet50-19c8e357.pth)
 

## Usage:
Open an image
- Filters -> RemoveBackground -> Background-remover

## Notes:
- In Gimp 2.99 new plugins do not get queried if they are not placed inside a subfolder. And sometimes they just dont get queried.
- Other than my RemoveBG plugin, this is using open source libraries and is working offline. But the results can be worse than the remove.bg ones.