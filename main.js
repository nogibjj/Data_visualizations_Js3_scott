// Fetch the state geometries
d3.json("US_States_with_Avg_Hourly_Rate.json").then(geoData => {

    console.log("GeoData:", geoData);  // Debugging line

    // Fetch your Average_Hourly_Rate.json
    d3.json("Average_Hourly_Rate.json").then(rateData => {

        console.log("RateData:", rateData);  // Debugging line

        // Map data by state name for easier lookup
        const rateByState = {};
        rateData.forEach(d => {
            rateByState[d.State] = +d.Average_Hourly_Rate;
        });

        const svg = d3.select("#hexbinSVG");
        const projection = d3.geoAlbersUsa()
            .fitSize([960, 600], geoData);
        const path = d3.geoPath().projection(projection);

        // Create the hexbin layout
        const hexbin = d3.hexbin()
            .radius(15)
            .extent([[0, 0], [960, 600]]);

        // Prepare the features
        const features = geoData.features.map(d => {
            const [x, y] = path.centroid(d);
            return {x, y, rate: rateByState[d.properties.NAME]};
        });

        console.log("Features:", features);  // Debugging line

        const color = d3.scaleSequential(d3.interpolateViridis)
            .domain([0, 6]);  // You can set your min-max domain here

        // Draw hexbins
        svg.append("g")
            .selectAll(".hexagon")
            .data(hexbin(features))
            .enter().append("path")
            .attr("class", "hexagon")
            .attr("d", hexbin.hexagon())
            .attr("transform", d => `translate(${d.x}, ${d.y})`)
            .attr("fill", d => color(d3.mean(d, f => f.rate)));
    });
});
