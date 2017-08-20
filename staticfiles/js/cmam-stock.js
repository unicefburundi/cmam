var app = angular.module('StockApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.controller('StockCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {
        
        // years
        $http.get("/cmam/get_year/")
        .then(function (response) {
          $scope.years = response.data;
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
        // province
        $http.get("/cmam/provinces/")
        .then(function (response) {
            if (response.data.length > 0) {
              var etablissements = [];
              for (var i = response.data.length - 1; i >= 0; i--) {
                var province = { 
                  name: response.data[i].name, 
                  code: response.data[i].code,
                  AMX: {
                    balance : i * 2 + 2,
                    sortie : i * 3 + 45,
                    reception : i * 4 + 21,
                  },
                  F75: {
                    balance : i * 5 + 51,
                    sortie : i * 6 + 471,
                    reception : i * 7 + 31,
                  },
                  ATPE: {
                    balance : i * 8 + 28,
                    sortie : i * 9 + 71,
                    reception : i * 10 + 251,
                  },
                  F100: {
                    balance : i * 11 + 311,
                    sortie : i * 12 + 61,
                    reception : i * 13 + 111,
                  },
                };
                etablissements.push(province);
              }
                console.log(etablissements);
                $scope.etablissements = etablissements;
            } 
        });
        $scope.update_province = function () {
            var province = $scope.dashboard.province;
            if (province) {
              $http.get("/cmam/provinces/" + province.code + "/" )
              .then(function (response) {
                $scope.etablissements = response.data.etablissements;
                $scope.districts = response.data.etablissements;
            });
          }
      };
          // district
          $scope.update_district = function () {
            var district = $scope.dashboard.district;
            if (district) {
              $http.get("/cmam/districts/" + district.code + "/" )
              .then(function (response) {
                  $scope.etablissements = response.data.etablissements;
                  $scope.cdss = response.data.etablissements;
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.dashboard.cds;
            if (cds) {
              $http.get("/cmam/cdss/" + cds.code + "/" )
              .then(function (response) {
                  $scope.etablissements = response.data.etablissements;
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
        };
}]);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
  }]);

