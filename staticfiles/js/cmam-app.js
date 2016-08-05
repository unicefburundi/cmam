var app = angular.module('myApp', []);
app.controller('myCtrl', ['$scope', '$http', function($scope, $http) {
            // products
            $http.get("/cmam/products/")
            .then(function (response) {
              $scope.produits = response.data;
          });
            $scope.update_product = function () {
                // $scope.produits = [$scope.sorties.products];
                console.log($scope.produits);
                $('#unites').html('<strong >' + $scope.sorties.products.general_measuring_unit +'</strong>');
            // $('#cen-entrees').html('<strong >' + unit.quantite_en_stock_central +'</strong>');
            //  $('#cen-sorties').html('<strong >' + unit.sortie +'</strong>');
            //  var reste = unit.quantite_en_stock_central - unit.sortie;
            //  $('#cen-restant').html('<strong >' + reste +'</strong>');
        };

          // province
          $http.get("/bdiadmin/province/")
          .then(function (response) {
              $scope.provinces = response.data;
          });
          $scope.update_province = function () {
            var unit = $scope.sorties.province;
            $http.get("/cmam/provinces/" + unit.code + "/" + $scope.sorties.products.id + "/")
            .then(function (response) {
              $scope.districts = response.data[0].districts;
          });
        };
        $scope.update_district = function () {
            var unit = $scope.sorties.district;
            $http.get("/cmam/districts/" + unit.code + "/" + $scope.sorties.products.id + "/")
            .then(function (response) {
              $scope.cds = response.data[0].cds;
          });
        };
        // Datepicker
        $scope.debut = '19/03/2013';
        $scope.fin = '19/03/2013';

    }]);

app.directive('datepicker', function() {
            return {
                restrict: 'A',
                require : 'ngModel',
                link : function (scope, element, attrs, ngModelCtrl) {
                    $(function(){
                        element.datepicker({
                            dateFormat:'dd/mm/yy',
                            onSelect:function (debut) {
                                scope.$apply(function () {
                                    ngModelCtrl.$setViewValue(debut);
                                    console.log($scope.debut)
                                });
                            }
                        });
                    });
                }
            };
        });