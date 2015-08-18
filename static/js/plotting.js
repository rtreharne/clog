var width = $("#plot").width();
var height = $("body").height();
console.log(width);
console.log(height);

function timelinePlot(input, stats) {

	var dataset = input,
		stats_input = stats;

	var eff = [];
	for (i = 0; i < dataset.length; i++) {
		dataset[i][4] = dataset[i][4].split('T')[0];
		eff.push(dataset[i][0]);
	}

	for (i = 0; i < stats_input.length; i++) {
		stats_input[i][0] = stats_input[i][0].split('T')[0];
	};

	console.log(stats_input)

	var maxEff = Math.max.apply(Math, eff)*1.1;

	var margin = {top: 10, right: 10, bottom: 100, left: 40},
	margin2 = {top: 430, right: 10, bottom: 20, left: 40},
	width = 960 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom,
	height2 = 500 - margin2.top - margin2.bottom;

	var padding = 40;

	var parseDate = d3.time.format.utc("%Y-%m-%d").parse;
	var mindate = parseDate("2015-07-10"),
		maxdate = parseDate("2015-08-05");

	var xMax = d3.max(dataset, function(d) {return parseDate(d[4]); });
	var xMin = d3.min(dataset, function(d) {return parseDate(d[4]); });

	
	var diff = (xMax.getTime()-xMin.getTime())*0.05;
	xMax.setTime(xMax.getTime() + (24*60*60*1000) + diff);
	xMin.setTime(xMin.getTime() -  (24*60*60*1000) - diff);

	var xScale = d3.time.scale()
		.domain([xMin, xMax])
		.range([0, width]);

	var xScale2 = d3.time.scale()
		.domain([xMin, xMax])
		.range([0, width]);

	var yScale = d3.scale.linear()
						  .domain([0, maxEff]) 
						  .range([height,0]);
	var yScale2 = d3.scale.linear()
	                      .domain([0, maxEff])
						  .range([height2,0]);


	var svg = d3.select("#plot")
		.append("svg")
		.attr('class', 'chart')
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom);

    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);

    var focus = svg.append("g")
        .attr("class", "focus")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var context = svg.append("g")
        .attr("class", "context")
        .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");
    
	var valueline = d3.svg.line()
		.x(function(d) { return xScale(parseDate(d[0])); })
		.y(function(d) { return yScale(d[1]); });

	var area = d3.svg.area()
		.interpolate("basis")
		.x(function(d) { return xScale(parseDate(d[0])); })
		.y(function(d) { return yScale(d[1]); })
	
	var xAxis = d3.svg.axis()
					  .scale(xScale)
					  .orient("bottom");

	var yAxis = d3.svg.axis()
					  .scale(yScale)
					  .orient("left")
	                  .ticks(5);

	var xAxis2 = d3.svg.axis().scale(xScale2).orient("bottom");
	
	focus.append("path")
		.attr("class", "line")
		.attr("d", area(stats_input));

    focus.append("g")
        .attr("class", "x axis")
        .attr("transform(0," + height + ")")

    context.append("g")
        .attr("class", "x axis")
		.attr("transform", "translate(0," + height2 + ")")
		.call(xAxis2);

	context.selectAll("circle")
	    .data(dataset)
		.enter()
		.append("circle")
		.attr("class", "dot")
		.attr("cx", function(d) {
			return xScale2(parseDate(d[4]));
		})
		.attr("cy", function (d) {
			return yScale2(d[0]);
		})
		.attr("r", 2);


	focus.selectAll("circle")
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

	focus.append("g")
	  .attr("class", "x axis")
	  .attr("transform", "translate(0," + height + ")")
	  .call(xAxis);

	focus.append("g")
	   .attr("class", "y axis")
	   .call(yAxis);
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

