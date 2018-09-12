var app = angular.module('StockApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(50);
  }]);

app.controller('stockCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout) {
    $scope.region = "Burundi";        
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

            if (province) {
                //update districts
                $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.etablissements;
                });
            } else {
                $scope.region = "Burundi";
                $scope.districts = null;
                $scope.cdss = null;
            }
        };
        
        // district
        $scope.update_district = function () {
            var district = $scope.district;
            if (district) {
            $scope.region = district.name;
              $http.get("/cmam/districts/" + district.code + "/" )
              .then(function (response) {
                  $scope.cds = response.data.etablissements;
                  $scope.cdss = response.data.etablissements;
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            $scope.region = cds.name;
            if (cds) {
              }
        };
        
        $scope.get_by_date = function () {
           // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
                $scope.districts = '';
                $scope.cdss = '';
              }
            });
        };
        
  }]);