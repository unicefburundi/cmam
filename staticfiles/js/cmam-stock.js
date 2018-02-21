var app = angular.module('StockApp', ['ngSanitize', 'datatables', 'datatables.buttons']);


function getsum (obj) {
  var AMX = {balance: 0, sortie: 0, reception: 0};
  var F75 = {balance: 0, sortie: 0, reception: 0};
  var ATPE = {balance: 0, sortie: 0, reception: 0};
  var F100 = {balance: 0, sortie: 0, reception: 0};
  obj.forEach( function (a) {
    AMX.balance += a.AMX.balance;
    AMX.sortie += a.AMX.sortie;
    AMX.reception += a.AMX.reception;
    F75.balance += a.F75.balance;
    F75.sortie += a.F75.sortie;
    F75.reception += a.F75.reception;
    ATPE.balance += a.ATPE.balance;
    ATPE.sortie += a.ATPE.sortie;
    ATPE.reception += a.ATPE.reception;
    F100.balance += a.F100.balance;
    F100.sortie += a.F100.sortie;
    F100.reception += a.F100.reception;
  });
  var somme = {AMX: AMX, F75: F75, ATPE: ATPE, F100: F100};
  return somme;
}

app.controller('StockCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {
        $scope.year = new Date().getFullYear();
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
                var somme = getsum(response.data[i].etablissements);
                var province = { 
                  name: response.data[i].name, 
                  code: response.data[i].code
                };
                etablissements.push($.extend(somme, province));
              }
                $scope.etablissements = etablissements;
                $scope.title = 'Province';
            } 
        });
        $scope.update_province = function () {
            $scope.title = "District";
            $scope.titles = "District";
            var province = $scope.dashboard.province;
            if (province) {
              $http.get("/cmam/provinces/" + province.code + "/"+ "?startdate=" + $scope.startdate + "&enddate=" + $scope.enddate )
              .then(function (response) {
                $scope.etablissements = response.data.etablissements;
                $scope.districts = response.data.etablissements;
            });
          }
      };
          // district
          $scope.update_district = function () {
            $scope.title = "CDS";
            $scope.titles = "Hopital";
            var district = $scope.dashboard.district;
            if (district) {
              $http.get("/cmam/districts/" + district.code + "/"+ "?startdate=" + $scope.startdate + "&enddate=" + $scope.enddate )
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
              $http.get("/cmam/cdss/" + cds.code + "/"+ "?startdate=" + $scope.startdate + "&enddate=" + $scope.enddate )
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
        $http.get("/cmam/provinces/"+ "?startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
          .then(function (response) {
              if (response.data.length > 0) {
                var etablissements = [];
                for (var i = response.data.length - 1; i >= 0; i--) {
                  var somme = getsum(response.data[i].etablissements);
                  var province = { 
                    name: response.data[i].name, 
                    code: response.data[i].code
                  };
                  etablissements.push($.extend(somme, province));
                }
                  $scope.etablissements = etablissements;
              } 
          });
        };
}]);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
  }]);

