var app = angular.module('ProgramApp', []);

app.controller('pgrmCtrl', ['$scope', '$http', function($scope, $http) {
    // in out reports
    $http.get("/cmam/inoutreport/")
    .then(function (response) {
        $scope.lesobjets =  response.data;
        console.log(response.data);
        var total_debut_semaine = 0;
        $.each(response.data, function () {
            total_debut_semaine += this.total_debut_semaine;
            }
        );
        console.log(total_debut_semaine);
        var weeks = {},
            columns = {},
            sumCols = ['total_debut_semaine','ptb', 'oedemes', 'rechute', 'readmission', 'transfert_interne_i','gueri', 'deces', 'abandon', 'non_repondant', 'transfert_interne_o'];

        $.each(data, function(index, obj) {
            if (!weeks[obj['week']]) {
                weeks[obj['week']] = {};
            }
            $.each(sumCols, function (index, col) {
                if (!weeks[obj['week']][col]) {
                    weeks[obj['week']][col] = 0;
                }
                if (!columns[col]) {
                    columns[col] = 0;
                }
                var val = parseFloat(obj[col]);
                if (!isNaN(val)) {
                    weeks[obj['week']][col] += val;
                    columns[col] += val;
                }
            });
        });
    });

        // province
        $http.get("/bdiadmin/province/")
          .then(function (response) {
                $scope.provinces = response.data;
          });
          $scope.update_province = function () {
            var province = $scope.province;
            $(".cds").hide();
            $(".district").show();
            if ($scope.province) {
              $http.get("/cmam/provinces/" + province.code + "/" )
                .then(function (response) {
                    $scope.districts = response.data.districts;
                  console.log($scope.districts);
              });
            }
        };
        // district
        $scope.update_district = function () {
            var district = $scope.district;
            if ($scope.province) {
              $http.get("/cmam/districts/" + district.code + "/" )
                .then(function (response) {
                  $scope.cds = response.data.cds;
                  console.log($scope.cds);
                  $(".cds").show();

              });
            }
        };
}]);

