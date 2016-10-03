var app = angular.module('ProgramApp', []);

app.controller('pgrmCtrl', ['$scope', '$http', function($scope, $http) {
    $http.get("/cmam/inoutreport/")
    .then(function (response) {
      $scope.lesobjets =  response.data;
    });
}]);

app.controller('FormCtrl', ['$scope', '$http', function($scope, $http) {
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
                  console.log($scope.districts);
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
                  $(".cds").show();

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

        // weeks
        $http.get("/cmam/get_week/")
        .then(function (response) {
          $scope.weeks = response.data;
        });

        $scope.update_years = function () {
        };

        $scope.update_weeks = function () {
        };
}]);
