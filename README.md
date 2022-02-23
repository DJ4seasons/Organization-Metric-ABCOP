# Organization-Metric-ABCOP
<br>
Python codes to calculate organization metric (index) ABCOP as well as other metrics like SCAI, MCAI, COP, and I_org for comparison. <br />
Reference: 2022JD036665 (AGU JGR-A; submitted) <br />
See also https://data.nasa.gov/Earth-Science/Tropical-CPR-identification-data-for-Organization-/md8t-ur38


### What to do
* For a given 2-D array of True/False (grid cell of object is marked as True),
* First, identify aggregates (options: diagonal connection or not; channel boundary condition or not)
* Second, calculate organization metrics based on identified aggregates.  
