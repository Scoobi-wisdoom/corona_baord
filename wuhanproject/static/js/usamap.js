$(function () {
// Create map instance
                var chart = am4core.create("chartdiv2", am4maps.MapChart);
// Disable zoom and pan
//     chart.maxZoomLevel = 1;
// chart.seriesContainer.draggable = false;
// chart.seriesContainer.resizable = false;
// Set map definition

                am4core.ready(function () {

// Themes begin
                    am4core.useTheme(am4themes_animated);
// Themes end

                    // Create map instance
                    var chart = am4core.create("chartdiv2", am4maps.MapChart);

// Set map definition
                    chart.geodata = am4geodata_usaLow;

// Set projection
                    chart.projection = new am4maps.projections.AlbersUsa();

                    chart.background.fill = am4core.color("#506b7c");
                    chart.background.fillOpacity = 1;
// Create map polygon series
                    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());


                    /* Create a heat rule */
                    polygonSeries.heatRules.push({
                        property: "fill",
                        target: polygonSeries.mapPolygons.template,
                        min: am4core.color("#dcea2e"),
                        max: am4core.color("#ff1700")
                    });


// Make map load polygon data (state shapes and names) from GeoJSON
                    polygonSeries.useGeodata = true;

// Set heatmap values for each state
                    var polygonArray = [];
                    $(".country").each(function (i, obj) {
                        var value_str_usa = $(obj).find(".case-usa").html();
                        var value_int_usa = parseInt(value_str_usa);


                        var value_recovered_usa = $(obj).find(".recovered-usa").html();
                        var value_confirmed_usa = $(obj).find(".case-usa").html();
                        var value_death_rate_usa = $(obj).find(".death-rate-usa").html();
                        var value_death_usa = $(obj).find(".death-usa").html();

                        var value_patients_usa = (parseInt(value_confirmed_usa) - parseInt(value_recovered_usa)) + "";
                        var fill_color_usa = "";

                        if (parseInt(value_confirmed_usa) < 5000) {
                            fill_color_usa = "#e0dc02";
                        } else if (parseInt(value_confirmed_usa) < 10000) {
                            fill_color_usa = "#b65f13";
                        } else if (parseInt(value_confirmed_usa) < 20000) {
                            fill_color_usa = "#aa0c00";
                        } else {
                            fill_color_usa = "#5b000a";
                        }

                        var item = {
                            "id": $(obj).find(".code-usa").html(),
                            "name": $(obj).find(".name-usa").html(),
                            "value": value_int_usa,
                            "fill": am4core.color(fill_color_usa),
                            "confirmed": value_confirmed_usa,
                            "recovered": value_recovered_usa,
                            "death": value_death_usa,
                            "patients": value_patients_usa,
                            "death_rate": value_death_rate_usa
                            // "recovered": recovered_str,
                        };
                        polygonArray.push(item);
                    });
                    polygonSeries.data = polygonArray;

// Configure series tooltip


// Configure series
                    var polygonTemplate = polygonSeries.mapPolygons.template;
                    polygonTemplate.tooltipText = "{name} \n Confirmed: {confirmed} \n Deaths: {death} \n Death%: {death_rate}% \n Recovered: {recovered}";
                    polygonTemplate.fillOpacity = 0.6;
                    polygonTemplate.nonScalingStroke = true;


                }); // end am4core.ready()
                chart.geodata = am4geodata_worldLow;

// Create map polygon series
                var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon (like country names) data from GeoJSON
                polygonSeries.useGeodata = true;

// Create hover state and set alternative fill color
                var hs = polygonTemplate.states.create("hover");

                hs.properties.fillOpacity = 0.9;

// Remove Antarctica
                polygonSeries.exclude = ["AQ"];

// Bind "fill" property to "fill" key in data
                polygonTemplate.propertyFields.fill = "fill";
// polygonTemplate.propertyFields.fill = "fill1";
                hs.propertyFields.fill = "fill";

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


            })

