var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
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
        };
}]);

app.controller('pgrmCtrl', ['$scope', '$http', function($scope, $http) {
    $http.get("/cmam/inoutreport/")
    .then(function (response) {
      $scope.lesobjets =  response.data;
    });

    $http({
        url: '/cmam/inoutreport/',
        method: "POST",
        data: { 'code' : 2 },
        headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
    .then(function(response) {
            // success
    },
    function(response) { // optional
            // failed
    });
}]);