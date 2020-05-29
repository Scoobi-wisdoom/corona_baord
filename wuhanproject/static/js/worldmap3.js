$(function () {
// Create map instance
    var chart = am4core.create("chartdiv1", am4maps.MapChart);
// Disable zoom and pan
//     chart.maxZoomLevel = 1;
// chart.seriesContainer.draggable = false;
// chart.seriesContainer.resizable = false;
// Set map definition
    chart.geodata = am4geodata_worldLow;

// Set projection
    chart.projection = new am4maps.projections.Miller();
    chart.background.fill = am4core.color("#506b7c");
    chart.background.fillOpacity = 1;
// Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon (like country names) data from GeoJSON
    polygonSeries.useGeodata = true;

// Configure series
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name} \n Confirmed: {confirmed} \n Deaths: {death} \n Death%: {death_rate}% \n Recovered: {recovered}";
    polygonTemplate.fillOpacity = 0.6;

// Create hover state and set alternative fill color
    var hs = polygonTemplate.states.create("hover");

    hs.properties.fillOpacity = 0.9;

// Remove Antarctica
    polygonSeries.exclude = ["AQ"];

// Bind "fill" property to "fill" key in data
    polygonTemplate.propertyFields.fill = "fill";
// polygonTemplate.propertyFields.fill = "fill1";
    hs.propertyFields.fill = "fill";

    /* Create a heat rule */
    polygonSeries.heatRules.push({
        property: "fill",
        target: polygonSeries.mapPolygons.template,
        min: am4core.color("#dcea2e"),
        max: am4core.color("#ff1700")
    });


    /* Create a heat legend */
    // add heat legend

    // var heatLegend = chart.chartContainer.createChild(am4maps.HeatLegend);
    // heatLegend.valign = "bottom";
    // heatLegend.align = "left";
    // heatLegend.width = am4core.percent(0);
    // heatLegend.series = polygonSeries;
    // heatLegend.orientation = "vertical";
    // heatLegend.padding(30, 30, 30, 30);
    // heatLegend.valueAxis.renderer.labels.template.fontSize = 10;
    // heatLegend.valueAxis.renderer.minGridDistance = 40;
    // heatLegend.minValue = 0;
    // heatLegend.maxValue = 10000;


// Add some data
    var polygonArray = [];
    $(".country").each(function (i, obj) {
        var value_str = $(obj).find(".case").html();
        var value_int = parseInt(value_str);


        var value_recovered = $(obj).find(".recovered").html();
        var value_confirmed = $(obj).find(".case").html();
        var value_death_rate = $(obj).find(".death-rate").html();
        var value_death = $(obj).find(".death").html();

        var value_patients = (parseInt(value_confirmed) - parseInt(value_recovered)) + "";
        var fill_color = "";

        if (parseInt(value_confirmed) < 5000) {
            fill_color = "#e0dc02";
        } else if (parseInt(value_confirmed) < 10000) {
            fill_color = "#b65f13";
        } else if (parseInt(value_confirmed) < 20000) {
            fill_color = "#aa0c00";
        } else {
            fill_color = "#5b000a";
        }

        var item = {
            "id": $(obj).find(".code").html(),
            "name": $(obj).find(".name").html(),
            "value": value_int,
            "fill": am4core.color(fill_color),
            "confirmed": value_confirmed,
            "recovered": value_recovered,
            "death": value_death,
            "patients": value_patients,
            "death_rate": value_death_rate
            // "recovered": recovered_str,
        };
        console.log(item);
        polygonArray.push(item);
    });
    console.log(polygonArray);
    polygonSeries.data = polygonArray;

})
