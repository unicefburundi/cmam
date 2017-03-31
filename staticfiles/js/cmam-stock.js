var app = angular.module('StockApp', ['ngSanitize']);

app.controller('StockCtrl', ['$scope', '$http', function($scope, $http) {
        // // products
        // $http.get("/cmam/products/")
        // .then(function (response) {
        //   $scope.etablissements = response.data;
        // });

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
  }]);

