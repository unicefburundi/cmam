var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
        // products
        $http.get("/cmam/products/")
        .then(function (response) {
          $scope.produits = response.data;
        });
        $scope.update_product = function () {
          $('#unites').html('<strong >' + $scope.dashboard.products.general_measuring_unit +'</strong>');
        };

          // province
          $http.get("/bdiadmin/province/")
          .then(function (response) {
              $scope.provinces = response.data;
          });
          $scope.update_province = function () {
            var unit = $scope.dashboard.province;
            if ($scope.dashboard.products) {
              $http.get("/cmam/provinces/" + unit.code + "/" + $scope.dashboard.products.id + "/")
                .then(function (response) {
                  $scope.districts = response.data[0].districts;
              });
              } else {
                $http.get("/cmam/provinces/" + unit.code + "/")
                  .then(function (response) {
                    $scope.districts = response.data.districts;
                });
              }
        };
          // district
        $scope.update_district = function () {
            var unit = $scope.dashboard.district;
            if ($scope.dashboard.products) {
              $http.get("/cmam/districts/" + unit.code + "/" + $scope.dashboard.products.id + "/")
                .then(function (response) {
                  $scope.cds = response.data[0].cds;
              });
              } else {
                $http.get("/cmam/districts/" + unit.code + "/" )
                  .then(function (response) {
                    $scope.cds = response.data.cds;
                    console.log($scope.cds);
                });
              }
        };
        // Datepicker
        $scope.debut = '19/03/2013';
        $scope.fin = '19/03/2013';

        // years
        $http.get("/cmam/get_year/")
        .then(function (response) {
          $scope.years = response.data;
        });

        $scope.update_years = function () {
          console.log($scope.dashboard.year);
        };
}]);

app.controller('pgrmCtrl', ['$scope', '$http', function($scope, $http) {
// products
    $http.get("/cmam/incoming/")
    .then(function (response) {
      $scope.incoming = response.data;
      console.log($scope.incoming);
    });
    $http.get("/cmam/outgoing/")
    .then(function (response) {
      $scope.outgoing = response.data;
      console.log($scope.outgoing);
    });
}]);