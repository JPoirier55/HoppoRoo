"""
    Module to hold highcharts customized data
"""

hc_quiz_view_json = {"global": {"useUTC": "false"},
                     "plotOptions": {"column": {"colorByPoint": "true"}},
                     "colors": ['#932933', '#00ED77', '#2E3B7F', '#FCF528']}

test_script = {"func": '''function test(){ console.log('this is a big test okakkykyky');}'''}

hc_quiz_view_body = '''{"chart": {"type": 'column',
                               "animation": 'Highcharts.svg',
                               "marginRight": 100,
                               "backgroundColor": "#F7F7CD"},
                               "events": {"load": function () {
                                var series = this.series[0];
                                var response_json;
                                setInterval(function () {
                                  $.when(
                                   $.ajax({
                                      type: json,
                                       url: "api/v1/data",
                                       success: function (response) {
                                         console.log(JSON.parse(response));
                                         response_json = JSON.parse(response);
                                        }
                                     }).then(function() {
                                        series.setData([response_json['A'] , response_json['B'],
                                        response_json['C'], response_json['D']], true, false, true);
                                    }))
                                }, 1000);
                            }},
                     "title": {"text": "",
                               "style": {
                                  "color": "#437341",
                                  "fontSize": "25px",
                                  "fontFamily": "teacher"}
                               },
                     "xAxis": {
                        "labels": {
                            "style": {
                                "color": "#932933",
                                "fontSize": "25px",
                                "fontFamily": "teacher"
                            }
                        },
                        "categories": [
                            'A',
                            'B',
                            'C',
                            'D',
                        ],
                    },
                    "yAxis": {
                        "title": {
                            "style": {
                                "color": "#932933",
                                "fontSize": "25px",
                                "fontFamily": "teacher"
                            },
                            "text": ""
                        },
                        "labels": {
                            "style": {
                                "color": "#437341",
                                "fontSize": "25px",
                                "fontFamily": "teacher"
                            }
                        },
                        "allowDecimals": false,
                    },

                    "legend": {
                        "enabled": false
                    },
                    "exporting": {
                        "enabled": false
                    },
                    "series": [{
                        "name": 'Choices',
                        "data": [1,2,3,4]

                    }]
                }'''