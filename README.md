# beam-load-analyse
##Program User Guide
<section>
<p>
This program is designed to analyse the load of a beam, but can be used for only fixed support beams.
</p>
In order to use program, you need to specify the following parameters:
<ul>
<li> Beam section type (rectangular, circular, I beam, T beam etc.)</li>
<li> Beam section spesific dimensions (width, height, thickness)</li>
<li> Loads list (point load, uniform load, distributed load)</li>
<li> Safety stress of the beam's material</li>
<li> Safety coefficient</li>
</ul>
!!!    If you want to load singular load, you need to set x_start and x_end values same.
</section>

##What you will get?
<section>
<p>
The program will give you the following results:
</p>
<ul>
<li> Load Distribution Diagram</li>
<li> Shear Force Diagram</li>
<li> Bending Moment Diagram</li>
<li> Tensile Stress Diagram</li>
<li> Shear Stress Diagram</li>
</ul>
</section>

##!!!Program is still in development!!!
<section>
<ul>
<li> You can't analyse torsion effects, in short this program neglects torsion effects.</li>
<li> You can't load in more than 1 axis. Other words, the point where the force is being applied can not be determined.</li>
<li> You can't load twice on the same location.</li>
</ul>
</section>
