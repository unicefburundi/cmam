function sortObject(o) {
    return Object.keys(o).sort().reduce((r, k) => (r[k] = o[k], r), {});
}

function getsum(response){
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
    weeks = sortObject(weeks);
    return [weeks, columns];
}

var app = angular.module('ProgramApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.directive("repeatEnd", function(){
	return {
		restrict: "A",
		link: function (scope, element, attrs) {
			if (scope.$last) {
				scope.$eval(attrs.repeatEnd);
			}
		}
	};
});

// global variable outside angular
var province1 = null, district1=null, cds1=null;

app.controller('pgrmCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
    $scope.year = new Date().getFullYear();
    // years
    $http.get("/cmam/get_year/")
    .then(function (response) {
      $scope.years = response.data;
    });
    // in out reports
    $http.get("/cmam/inoutreport/?facility__facility_level__name=CDS")
    .then(function (response) {
         var sums = getsum(response);
        $scope.lescds =  sums[0];
        $scope.cdsgnrl = sums[1];
        $scope.sommecds = sums[1];
    });
    $http.get("/cmam/inoutreport/?facility__facility_level__name=Hospital")
    .then(function (response) {
        var sums = getsum(response);
        $scope.leshopitaux =  sums[0];
        $scope.hopitauxgnrl =  sums[1];
        $scope.sommehopitaux = sums[1];
    });
		
		// province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            } else {
                $("#province-group").hide();
                $http.get("/cmam/districts/")
                .then(function (response) {
                    $scope.districts = response.data;
                });
            }
        });

        $scope.update_province = function () {
            var province = $scope.province;
            $scope.province1 = province;
            $scope.district1 = null;
            $scope.cds1 = null;
            if ($scope.province) {
                $scope.cdscds =  0;
                $scope.hopitauxcds =  0;
                $scope.cdsdistr =  0;
                $scope.hopitauxdistr =  0;
                //update districts
                $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.etablissements;
                });

                // update hopitaux
                $http.get("/cmam/inoutreport/?search=" + province.code+ "&facility__facility_level__name=Hospital" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
                .then(function (response) {
                    var sums = getsum(response);
                    $scope.leshopitaux =  sums[0];
                    $scope.hopitauxprov =  sums[1];
                    $scope.sommehopitaux = sums[1];
                });
                // update cds
                $http.get("/cmam/inoutreport/?search=" + province.code+ "&facility__facility_level__name=CDS" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
                .then(function (response) {
                    var sums = getsum(response);
                    $scope.lescds =  sums[0];
                    $scope.cdsprov =  sums[1];
                    $scope.sommecds = sums[1];
                });
            }
        };
		
        // district
        $scope.update_district = function () {
            var district = $scope.district;
            $scope.district1 = district;
            $scope.cds1 = null;
            if ($scope.district) {
              $http.get("/cmam/districts/" + district.code + "/" )
              .then(function (response) {
                  $scope.cds = response.data.etablissements;
                  $scope.cdss = response.data.etablissements;
              });
            $scope.cdscds =  0;
            $scope.hopitauxcds =  0;
            // update cds
            $http.get("/cmam/inoutreport/?search=" + district.code+ "&facility__facility_level__name=CDS" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
            .then(function (response) {
                var sums = getsum(response);
                $scope.lescds =  sums[0];
                $scope.cdsdistr =  sums[1];
                $scope.sommecds = sums[1];
            });
            // update hopitaux
            $http.get("/cmam/inoutreport/?search=" + district.code+ "&facility__facility_level__name=Hospital" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
            .then(function (response) {
                var sums = getsum(response);
                $scope.leshopitaux =  sums[0];
                $scope.hopitauxdistr =  sums[1];
                $scope.sommehopitaux = sums[1];
            });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            $scope.cds1 = cds;
            if (cds) {
                // update cds
                $http.get("/cmam/inoutreport/?search=" + cds.code+ "&facility__facility_level__name=CDS" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
                .then(function (response) {
                    var sums = getsum(response);
                    $scope.lescds =  sums[0];
                    $scope.cdscds =  sums[1];
                    $scope.sommecds = sums[1];
                });
                // update hopitaux
                $http.get("/cmam/inoutreport/?search=" + cds.code+ "&facility__facility_level__name=Hospital" + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
                .then(function (response) {
                    var sums = getsum(response);
                    $scope.leshopitaux =  sums[0];
                    $scope.hopitauxcds =  sums[1];
                    $scope.sommehopitaux = sums[1];
                });
              }
        };
		
		$scope.update_years = function () {
           // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
                $scope.districts = '';
                $scope.cdss = '';
              }
            });
          // in out reports
            $http.get("/cmam/inoutreport/?facility__facility_level__name=CDS"+ "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
            .then(function (response) {
                 var sums = getsum(response);
                $scope.lescds =  sums[0];
                $scope.cdsgnrl = sums[1];
                $scope.sommecds = sums[1];
            });
            $http.get("/cmam/inoutreport/?facility__facility_level__name=Hospital"+ "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
            .then(function (response) {
                var sums = getsum(response);
                $scope.leshopitaux =  sums[0];
                $scope.hopitauxgnrl =  sums[1];
                $scope.sommehopitaux = sums[1];
            });
        };
		
  }]);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
  }]);
