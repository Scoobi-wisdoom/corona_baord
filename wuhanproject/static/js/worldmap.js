$(function () {
// Create map instance
    var chart = am4core.create("chartdiv1", am4maps.MapChart);
// Disable zoom and pan
    chart.maxZoomLevel = 1;
    chart.seriesContainer.draggable = false;
    chart.seriesContainer.resizable = false;
// Set map definition
    chart.geodata = am4geodata_worldLow;

// Set projection
    chart.projection = new am4maps.projections.Miller();

// Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon (like country names) data from GeoJSON
    polygonSeries.useGeodata = true;

// Configure series
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name} \n confirmed: {value.value.formatNumber('#')}";
    polygonTemplate.fillOpacity = 0.6;

// Create hover state and set alternative fill color
    var hs = polygonTemplate.states.create("hover");

    hs.properties.fillOpacity = 0.9;

// Remove Antarctica
    polygonSeries.exclude = ["AQ"];

// Bind "fill" property to "fill" key in data
    polygonTemplate.propertyFields.fill = "fill";
    polygonTemplate.propertyFields.fill = "fill1";
    hs.propertyFields.fill = "fill1";

    /* Create a heat rule */
    polygonSeries.heatRules.push({
        property: "fill",
        target: polygonSeries.mapPolygons.template,
        min: am4core.color("#eaa459"),
        max: am4core.color("#ff2a2f")
    });


    /* Create a heat legend */
// add heat legend
    var heatLegend = chart.chartContainer.createChild(am4maps.HeatLegend);
    heatLegend.valign = "bottom";
    heatLegend.align = "left";
    heatLegend.width = am4core.percent(25);
    heatLegend.series = polygonSeries;
    heatLegend.orientation = "vertical";
    heatLegend.padding(30, 30, 30, 30);
    heatLegend.valueAxis.renderer.labels.template.fontSize = 10;
    heatLegend.valueAxis.renderer.minGridDistance = 40;
    heatLegend.minValue = 0;
    heatLegend.maxValue = 12000;


// Add some data
    var polygonArray = [];
    $(".country").each(function (i, obj) {
        var value_int = $(obj).find(".case").html()
        var item = {
            "id": $(obj).find(".code").html(),
            "name": $(obj).find(".name").html(),
            "value": parseInt(value_int)
        };
        console.log(item);
        polygonArray.push(item);
    });
    console.log(polygonArray);
    polygonSeries.data = polygonArray;

})
