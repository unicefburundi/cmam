var app = angular.module('StockApp', ['ngSanitize']);
app.controller('StockCtrl', ['$scope', '$http', function($scope, $http) {
        // products
        $http.get("/cmam/products/")
        .then(function (response) {
          $scope.produits = response.data;
        });

        // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
              $scope.provinces = response.data;
          });
          $scope.update_province = function () {
            var province = $scope.dashboard.province;
            $(".cds").hide();
            $(".district").show();
            if ($scope.produits) {
              $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.districts;
              });
            }
        };
          // district
        $scope.update_district = function () {
            var district = $scope.dashboard.district;
            if ($scope.dashboard.province) {
              $http.get("/cmam/districts/" + district.code + "/" )
                .then(function (response) {
                  $scope.cds = response.data.cds;
                  console.log($scope.cds);
                  $scope.cdss = response.data.cds;
                  $(".cds").show();
              });
              }
        };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.dashboard.cds;
            if (cds) {
              $http.get("/cmam/cdss/" + cds['code'] + "/" )
                .then(function (response) {
                  $scope.cds = response.data.products;
                  console.log(response.data.products[0]);
              });
              }
        };
}]);

