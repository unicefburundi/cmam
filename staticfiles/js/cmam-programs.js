var app = angular.module('ProgramApp', []);

app.controller('pgrmCtrl', ['$scope', '$http', function($scope, $http) {
    // in out reports
    $http.get("/cmam/inoutreport/?report__facility__facility_level__name=CDS")
    .then(function (response) {
        var weeks = {},
        columns = {},
        sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'], data = response.data;

        $.each(data, function(index, obj) {
            if (!weeks[obj['week']]) {
                weeks[obj['week']] = {};
            }
            $.each(sumCols, function (index, col) {
                if (!weeks[obj['week']][col]) {
                    weeks[obj['week']][col] = 0;
                }
                if (!columns[col]) {
                    columns[col] = 0;
                }
                var val = parseFloat(obj[col]);
                if (!isNaN(val)) {
                    weeks[obj['week']][col] += val;
                    columns[col] += val;
                }
            });
        });
        $scope.lescds =  weeks;
        $scope.cdsgnrl = columns;
        $scope.sommecds = columns;
    });

    $http.get("/cmam/inoutreport/?report__facility__facility_level__name=Hospital")
    .then(function (response) {
        var weeks = {},
        columns = {},
        sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'], data = response.data;

        $.each(data, function(index, obj) {
            if (!weeks[obj['week']]) {
                weeks[obj['week']] = {};
            }
            $.each(sumCols, function (index, col) {
                if (!weeks[obj['week']][col]) {
                    weeks[obj['week']][col] = 0;
                }
                if (!columns[col]) {
                    columns[col] = 0;
                }
                var val = parseFloat(obj[col]);
                if (!isNaN(val)) {
                    weeks[obj['week']][col] += val;
                    columns[col] += val;
                }
            });
        });

        $scope.leshopitaux =  weeks;
        $scope.hopitauxgnrl =  columns;
        $scope.sommehopitaux = columns;
    });

        // province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            $scope.provinces = response.data;
        });

        $scope.update_province = function () {
            var province = $scope.province;
            if (province.code <2){
                console.log("0"+province.code + " short");
            } else {
                console.log(province);
            }
            if ($scope.province) {

                //update districts
                $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.districts;
                });

                // update hopitaux
                $http.get("/cmam/inoutreport/?search=" + province.code+ "&report__facility__facility_level__name=Hospital")
                .then(function (response) {
                    var weeks = {},
                    columns = {},
                    sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'],
                    data = response.data;

                    $.each(data, function(index, obj) {
                        if (!weeks[obj['week']]) {
                            weeks[obj['week']] = {};
                        }
                        $.each(sumCols, function (index, col) {
                            if (!weeks[obj['week']][col]) {
                                weeks[obj['week']][col] = 0;
                            }
                            if (!columns[col]) {
                                columns[col] = 0;
                            }
                            var val = parseFloat(obj[col]);
                            if (!isNaN(val)) {
                                weeks[obj['week']][col] += val;
                                columns[col] += val;
                            }
                        });
                    });

                    $scope.leshopitaux =  weeks;
                    $scope.hopitauxprov =  columns;
                    $scope.sommehopitaux = columns;
                });
                // update cds
                $http.get("/cmam/inoutreport/?search=" + province.code+ "&report__facility__facility_level__name=CDS")
                .then(function (response) {
                    var weeks = {},
                    columns = {},
                    sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'],
                    data = response.data;

                    $.each(data, function(index, obj) {
                        if (!weeks[obj['week']]) {
                            weeks[obj['week']] = {};
                        }
                        $.each(sumCols, function (index, col) {
                            if (!weeks[obj['week']][col]) {
                                weeks[obj['week']][col] = 0;
                            }
                            if (!columns[col]) {
                                columns[col] = 0;
                            }
                            var val = parseFloat(obj[col]);
                            if (!isNaN(val)) {
                                weeks[obj['week']][col] += val;
                                columns[col] += val;
                            }
                        });
                    });
                    $scope.lescds =  weeks;
                    $scope.cdsprov =  columns;
                    $scope.sommecds = columns;
                });
            }
        };

        // district
        $scope.update_district = function () {
            var district = $scope.district;
            if ($scope.district) {
              $http.get("/cmam/districts/" + district.code + "/" )
              .then(function (response) {
                  $scope.cds = response.data.cds;
              });

              // update cds
              $http.get("/cmam/inoutreport/?search=" + district.code+ "&report__facility__facility_level__name=CDS")
                .then(function (response) {
                    var weeks = {},
                    columns = {},
                    sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'],
                    data = response.data;

                    $.each(data, function(index, obj) {
                        if (!weeks[obj['week']]) {
                            weeks[obj['week']] = {};
                        }
                        $.each(sumCols, function (index, col) {
                            if (!weeks[obj['week']][col]) {
                                weeks[obj['week']][col] = 0;
                            }
                            if (!columns[col]) {
                                columns[col] = 0;
                            }
                            var val = parseFloat(obj[col]);
                            if (!isNaN(val)) {
                                weeks[obj['week']][col] += val;
                                columns[col] += val;
                            }
                        });
                    });
                    $scope.lescds =  weeks;
                    $scope.cdsdistr =  columns;
                    $scope.sommecds = columns;
                });
              // update hopitaux
              $http.get("/cmam/inoutreport/?search=" + district.code+ "&report__facility__facility_level__name=Hospital")
                .then(function (response) {
                    var weeks = {},
                    columns = {},
                    sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'],
                    data = response.data;

                    $.each(data, function(index, obj) {
                        if (!weeks[obj['week']]) {
                            weeks[obj['week']] = {};
                        }
                        $.each(sumCols, function (index, col) {
                            if (!weeks[obj['week']][col]) {
                                weeks[obj['week']][col] = 0;
                            }
                            if (!columns[col]) {
                                columns[col] = 0;
                            }
                            var val = parseFloat(obj[col]);
                            if (!isNaN(val)) {
                                weeks[obj['week']][col] += val;
                                columns[col] += val;
                            }
                        });
                    });

                    $scope.leshopitaux =  weeks;
                    $scope.hopitauxdistr =  columns;
                    $scope.sommehopitaux = columns;
                });
          }
      };
  }]);

