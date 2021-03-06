Roadmap_Poly2tri
========

Construct roadmap from triangulation of polygon workspace

```
@INPROCEEDINGS{8264271,
  author={M. {Guo} and M. M. {Zavlanos}},
  booktitle={2017 IEEE 56th Annual Conference on Decision and Control (CDC)}, 
  title={Temporal task planning in wirelessly connected environments with unknown channel quality}, 
  year={2017},
  volume={},
  number={},
  pages={4161-4168},
  doi={10.1109/CDC.2017.8264271}}
```

-----
Description
-----
this package generates a roadmap for autonomous robots within a 2D polygon workspace.

-----
Features
-----
* Takes a 2D workspace with any number of non-overlaping polygon obstacles
* Triangulation over the workspace by poly2tri
* Generate waypoints and raodmap for the robot to navigate within the workspace

<p align="center">  
  <img src="https://github.com/MengGuo/Roadmap_Poly2tri/blob/master/data/example.png" width="800"/>
</p>

----
Dependence
----
* install [poly2tri.python] (https://github.com/davidcarne/poly2tri.python)
