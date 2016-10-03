var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
        // products
        $http.get("/cmam/products/")
        .then(function (response) {
          $scope.produits = response.data;
          $scope.disto = 2;
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