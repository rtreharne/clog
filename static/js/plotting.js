var width = $("#plot").width();
var height = $("body").height();
console.log(width);
console.log(height);
function timelinePlot(input) {

	var dataset = input;
	var eff = [];
	for (i = 0; i < dataset.length; i++) {
		dataset[i][4] = dataset[i][4].split('T')[0];
		eff.push(dataset[i][0]);
	}

	var maxEff = Math.max.apply(Math, eff)*1.1;

	var w = width;
	var h = height * 0.6;
	var padding = 40;

	var parseDate = d3.time.format.utc("%Y-%m-%d").parse;
	var mindate = parseDate("2015-07-10"),
		maxdate = parseDate("2015-08-05");

	var xMax = d3.max(dataset, function(d) {return parseDate(d[4]); });
	var xMin = d3.min(dataset, function(d) {return parseDate(d[4]); });

	
	var diff = (xMax.getTime()-xMin.getTime())*0.05
	xMax.setTime(xMax.getTime() + (24*60*60*1000) + diff);
	xMin.setTime(xMin.getTime() -  (24*60*60*1000) - diff);

	var xScale = d3.time.scale()
		.domain([xMin, xMax])
		.range([padding, w - padding]);

	var yScale = d3.scale.linear()
						  .domain([0, maxEff]) 
		//.domain([0, d3.max(dataset, function (d) {
			// return d[0];
	   // })])
						 .range([h - padding, padding]);

	var svg = d3.select("#plot")
		.append("svg")
		.attr('class', 'chart')
		.attr("width", w)
		.attr("height", h);
	
	var xAxis = d3.svg.axis()
					  .scale(xScale)
					  .orient("bottom");

	var yAxis = d3.svg.axis()
					  .scale(yScale)
					  .orient("left")
	                  .ticks(5);

	svg.selectAll("circle")
		.data(dataset)
		.enter()
		.append("circle")
		.attr("id", function(d) {return d[5];})
		.attr("cx", function(d) {
			return xScale(parseDate(d[4]));
		})
		.attr("cy", function (d) {
			return yScale(d[0]);
		})
		.attr("r", 8)    
		.on("click", function(d){ window.location.replace(d3.select(this).attr("id")) }, 'id');

	svg.append("g")
	  .attr("class", "axis")
	  .attr("transform", "translate(0," + (h - padding) + ")")
	  .call(xAxis);

	svg.append("g")
	   .attr("class", "axis")
	   .attr("transform", "translate(" + padding + ",0)")
	   .call(yAxis)
	   .append("text")
	   .attr("class", "label")
	   .attr("transform", "rotate(-90)")
	   .attr("dy", "0.71em")
	   .attr("y", 10)
	   .attr("x", -padding)
	   .style("text-anchor", "end")
	   .text("Efficiency (%)");
}

function jvPlot(file) {

	var w = $('#plot').width();
	var h = height * 0.6;
	var padding = 40;

	var file = '/media/'+ file;

	d3.text(file, 'text/csv', function(csv) {
		// remove comment rows with regex - not fully tested, but should work
		csv = csv.replace((/^[#@][^\r\n]+[\r\n]+/mg), '');
		// replace commas with spaces
		csv = csv.replace(/[ ,]+/g, ",");
		// parse data to array
		var dataset = d3.csv.parseRows(csv).map(function(row) {
			return row.map(function(value) {
				return +value;
			});
		
		});
		for(var i=0; i<dataset.length; i++) {
			dataset[i][1] *= 4000;
			}

		var svg = d3.select("#plot")
					.append("svg")
					.attr("width", w)
					.attr("height", h)
	
		var xScale = d3.scale.linear()
							  .domain([d3.min(dataset, function(d) { return d[0]; } ), d3.max(dataset, function(d) { return d[0]; } )]) 
			.range([padding, w - padding]);

		var yScale = d3.scale.linear()
							  .domain([d3.min(dataset, function(d) { return d[1]; } ), d3.max(dataset, function(d) { return d[1]; } )]) 
							 .range([h - padding, padding]);

		var line = d3.svg.line()
			.x(function(d) {return xScale(d[0]);})
			.y(function(d) {return yScale(d[1]);});

		var xAxis = d3.svg.axis()
						  .scale(xScale)
						  .orient("bottom")
						  .ticks(5);

		var yAxis = d3.svg.axis()
						  .scale(yScale)
						  .orient("left")
						  .ticks(5);

		svg.selectAll("circle")
		   .data(dataset)
		   .enter()
		   .append("circle")
		   .attr("cx", function(d) { return xScale(d[0]) })
		   .attr("cy", function(d) { return yScale(d[1]) })
		   .attr("r", 2);

		svg.append("path")
		   .attr("d", line(dataset))
	
		svg.append("g")
		  .attr("class", "axis")
		  .attr("transform", "translate(0," + (h - padding) + ")")
		  .call(xAxis)

		svg.append("g")
		  .attr("class", "axis")
		  .attr("transform", "translate(" + padding + ",0)")
		  .call(yAxis)
		  
	});
}

