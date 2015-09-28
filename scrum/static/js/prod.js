var app, get_utc_date, get_utc_datetime, set_utc_date, set_utc_datetime;

moment.locale('fr');

$.ajaxSetup({
  headers: {
    "X-CSRFToken": $.cookie('csrftoken')
  }
});

app = angular.module('app', ['ngRoute', 'ngResource', 'ui.sortable', 'dndLists']);

$.fn.datetimepicker.dates['en'] = {
  days: ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"],
  daysShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"],
  daysMin: ["D", "L", "Ma", "Me", "J", "V", "S", "D"],
  months: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aot", "Septembre", "Octobre", "Novembre", "Décembre"],
  monthsShort: ["Jan", "Fev", "Mar", "Avr", "Mai", "Jui", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"],
  today: "Aujourd'hui",
  suffix: [],
  meridiem: ["matin", "aprem"],
  weekStart: 1,
  format: 'dd/mm/yyyy hh:ii',
  autoclose: true
};

app.config(function($routeProvider, $interpolateProvider, $httpProvider, $resourceProvider) {
  $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie('csrftoken');
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $interpolateProvider.startSymbol('~{');
  $interpolateProvider.endSymbol('}~');
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  $resourceProvider.defaults.stripTrailingSlashes = false;
  $routeProvider.when('/backlog', {
    templateUrl: '/backlog',
    controller: 'BacklogController',
    title: 'Backlog'
  }).when('/sprint', {
    templateUrl: '/sprint',
    controller: 'SprintController',
    title: 'Sprint'
  }).otherwise({
    redirectTo: '/backlog'
  });
});

app.factory('Task', [
  '$resource', function($resource) {
    return $resource('/api/task/:id', {
      id: '@id'
    }, {
      'update': {
        method: 'PUT',
        params: {
          id: '@id'
        }
      },
      'query': {
        method: 'GET',
        isArray: false
      }
    });
  }
]);

app.factory('Sprint', [
  '$resource', function($resource) {
    return $resource('/api/sprint/:id', {
      id: '@id'
    }, {
      'update': {
        method: 'PUT',
        params: {
          id: '@id'
        }
      },
      'query': {
        method: 'GET',
        isArray: false
      }
    });
  }
]);

app.factory('Employee', [
  '$resource', function($resource) {
    return $resource('/api/employee/:id', {
      id: '@id'
    }, {
      'update': {
        method: 'PUT',
        params: {
          id: '@id'
        }
      },
      'query': {
        method: 'GET',
        isArray: false
      }
    });
  }
]);

app.filter("get_utc_datetime", function() {
  return function(date) {
    return get_utc_datetime(date);
  };
});

app.filter("get_utc_date", function() {
  return function(date) {
    return get_utc_date(date);
  };
});

get_utc_datetime = function(date) {
  var d;
  d = moment(date, moment.ISO_8601).utc();
  if (d.isValid()) {
    return d.format("DD/MM/YYYY HH:mm");
  } else {
    return "";
  }
};

get_utc_date = function(date) {
  var d;
  d = moment(date, "YYYY-MM-DD");
  if (d.isValid()) {
    return d.format("DD/MM/YYYY");
  } else {
    return "";
  }
};

set_utc_datetime = function(date) {
  if (date === "" || date === void 0) {
    return "";
  } else {
    return moment(date, "DD/MM/YYYY HH:mm").format("YYYY-MM-DDTHH:mm:ss") + "Z";
  }
};

set_utc_date = function(date) {
  if (date === "" || date === void 0) {
    return "";
  } else {
    return moment(date, "DD/MM/YYYY").format("YYYY-MM-DD");
  }
};

var BacklogController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

BacklogController = (function() {
  BacklogController.$inject = ['$scope', '$rootScope', 'Task', 'Employee', '$http'];

  function BacklogController(scope, $rootScope, Task, $http) {
    this.scope = scope;
    this.get_tasks = bind(this.get_tasks, this);
    this.get_tasks_selected = bind(this.get_tasks_selected, this);
    this.run_action = bind(this.run_action, this);
    this.modal_task = bind(this.modal_task, this);
    this.Task = Task;
    this.http = $http;
    this.rootScope = $rootScope;
    this.scope.tasks = this.get_tasks();
    this.scope.run_modal = this.run_modal;
    this.scope.run_action = this.run_action;
    this.scope.modal_task = this.modal_task;
    this.scope.$on("task_recorded", (function(_this) {
      return function() {
        return _this.get_tasks();
      };
    })(this));
    this.scope.sortableOptions = {
      stop: (function(_this) {
        return function(e, ui) {
          var i, j, len, new_index, positions, ref, task;
          new_index = ui.item.index();
          task = _this.scope.tasks[new_index];
          positions = [];
          ref = _this.scope.tasks;
          for (i = j = 0, len = ref.length; j < len; i = ++j) {
            task = ref[i];
            positions.push(task.id);
          }
          $.post("/task/change_priority/" + task.id, {
            'positions': positions.join(":")
          }, function(r) {
            _this.get_tasks();
            alertify.success("Changement de priorité effectué avec succès");
            return true;
          });
          return true;
        };
      })(this)
    };
    true;
  }

  BacklogController.prototype.modal_task = function(task) {
    this.rootScope.$broadcast('modal_task', task || {});
    return true;
  };

  BacklogController.prototype.run_action = function(action) {
    var data, item, tasks_selected;
    tasks_selected = this.get_tasks_selected();
    if (tasks_selected.length === 0) {
      alertify.alert("Veuillez sélectionner des tâches");
      return true;
    }
    data = {
      'ids': ((function() {
        var j, len, results;
        results = [];
        for (j = 0, len = tasks_selected.length; j < len; j++) {
          item = tasks_selected[j];
          results.push(item.id);
        }
        return results;
      })()).join(':'),
      'action': action
    };
    if (action === "sprint_prompt") {
      $('#modal_run_action_options').modal('show');
      return true;
    } else if (action === "sprint") {
      data.sprint = this.scope.run_action_option.sprint;
    } else if (action === "delete_confirm") {
      alertify.confirm("Êtes-vous sur de vouloir supprimer les tâches sélectionnées?", (function(_this) {
        return function() {
          _this.scope.run_action('delete');
          return true;
        };
      })(this));
      return true;
    }
    $.post("/task/actions/", data, (function(_this) {
      return function(r) {
        _this.get_tasks();
        alertify.success("Action effectuée avec succès!");
        return true;
      };
    })(this));
    return true;
  };

  BacklogController.prototype.get_tasks_selected = function() {
    return $.grep(this.scope.tasks, function(item, n) {
      return item.checked != null;
    });
  };

  BacklogController.prototype.get_tasks = function() {
    this.scope.tasks = this.Task.query();
    return this.scope.tasks.$promise.then((function(_this) {
      return function(result) {
        _this.scope.tasks = result.results;
        return true;
      };
    })(this));
  };

  return BacklogController;

})();

app.controller('BacklogController', BacklogController);

var MenuController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

MenuController = (function() {
  MenuController.$inject = ['$scope', '$location'];

  function MenuController(scope, $location) {
    this.scope = scope;
    this.logout = bind(this.logout, this);
    this.scope.logout = this.logout;
    this.scope.$on('loaderShow', (function(_this) {
      return function() {
        _this.scope.showLoader = true;
        return true;
      };
    })(this));
    this.scope.$on('loaderHide', (function(_this) {
      return function() {
        _this.scope.showLoader = false;
        return true;
      };
    })(this));
    this.scope.menu_is_active = (function(_this) {
      return function(route) {
        return route === $location.path();
      };
    })(this);
  }

  MenuController.prototype.logout = function() {
    if (window.confirm("Êtes-vous sûr de vouloir quitter le site?")) {
      return window.location = "/logout";
    }
  };

  return MenuController;

})();

app.controller('MenuController', MenuController);

var SprintController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

SprintController = (function() {
  SprintController.$inject = ['$scope', '$rootScope', 'Task', 'Sprint', '$http', '$q'];

  function SprintController(scope, $rootScope, Task, Sprint, $http, $q) {
    this.scope = scope;
    this.delete_sprint = bind(this.delete_sprint, this);
    this.record_sprint = bind(this.record_sprint, this);
    this.modal_update_sprint = bind(this.modal_update_sprint, this);
    this.modal_new_sprint = bind(this.modal_new_sprint, this);
    this.modal_init = bind(this.modal_init, this);
    this.modal_task = bind(this.modal_task, this);
    this.get_list_task = bind(this.get_list_task, this);
    this.task_dropped = bind(this.task_dropped, this);
    this.load_tasks = bind(this.load_tasks, this);
    this.init_tasks = bind(this.init_tasks, this);
    this.Sprint = Sprint;
    this.Task = Task;
    this.scope.tasks = [];
    this.scope.sprints = [];
    this.scope.modal_new_sprint = this.modal_new_sprint;
    this.scope.record_sprint = this.record_sprint;
    this.scope.modal_update_sprint = this.modal_update_sprint;
    this.scope.delete_sprint = this.delete_sprint;
    this.scope.modal_task = this.modal_task;
    this.scope.task_dropped = this.task_dropped;
    this.q = $q;
    this.rootScope = $rootScope;
    $('#modal_sprint .datetimepicker2').datetimepicker({
      minView: 'month',
      format: 'dd/mm/yyyy',
      autoclose: true
    });
    this.init_tasks();
    this.scope.$on("task_recorded", (function(_this) {
      return function(event, task) {
        _this.load_tasks().then(function() {
          var t;
          t = _this.get_list_task(task);
          if (t) {
            t.label = task.name;
          }
          return true;
        });
        return true;
      };
    })(this));
    this.load_tasks();
    true;
  }

  SprintController.prototype.init_tasks = function() {
    this.scope.models = {
      selected: null,
      lists: [[], [], []]
    };
    return true;
  };

  SprintController.prototype.load_tasks = function() {
    var deferred;
    deferred = this.q.defer();
    this.init_tasks();
    this.get_sprints().then((function(_this) {
      return function(r) {
        var last_sprint;
        if (r.results.length) {
          last_sprint = r.results[0];
          _this.get_tasks(last_sprint.id).then(function(tasks) {
            var k, len, results, task;
            results = [];
            for (k = 0, len = tasks.length; k < len; k++) {
              task = tasks[k];
              results.push(_this.scope.models.lists[task.status].push({
                id: task.id,
                label: task.name
              }));
            }
            return results;
          });
        }
        deferred.resolve(r);
        return true;
      };
    })(this));
    return deferred.promise;
  };

  SprintController.prototype.task_dropped = function(event, index, task, $index) {
    var new_task;
    new_task = {
      'id': task.id,
      'status': $index
    };
    $.post("task/change_status/" + task.id, new_task, (function(_this) {
      return function() {
        return true;
      };
    })(this));
    return task;
  };

  SprintController.prototype.get_list_task = function(init_task) {
    var i, j, ref, task, tasks;
    ref = this.scope.models.lists;
    for (i in ref) {
      tasks = ref[i];
      for (j in tasks) {
        task = tasks[j];
        if (task.id === init_task.id) {
          return task;
        }
      }
    }
    return null;
  };

  SprintController.prototype.modal_task = function(task) {
    this.rootScope.$broadcast('modal_task', task || {});
    return true;
  };

  SprintController.prototype.get_sprints = function() {
    var deferred;
    deferred = this.q.defer();
    this.Sprint.query().$promise.then((function(_this) {
      return function(r) {
        _this.scope.sprints = r.results;
        return deferred.resolve(r);
      };
    })(this));
    return deferred.promise;
  };

  SprintController.prototype.get_tasks = function(sprint) {
    var deferred;
    deferred = this.q.defer();
    $.post("/sprint/tasks/" + sprint, (function(_this) {
      return function(r) {
        return deferred.resolve(r);
      };
    })(this));
    return deferred.promise;
  };

  SprintController.prototype.modal_init = function() {
    this.scope.sprint_selected = {};
    return true;
  };

  SprintController.prototype.modal_new_sprint = function() {
    this.modal_init();
    $('#modal_sprint').modal('show');
    return true;
  };

  SprintController.prototype.modal_update_sprint = function(sprint) {
    this.scope.sprint_selected = angular.copy(sprint);
    this.scope.sprint_selected.date_start = get_utc_date(this.scope.sprint_selected.date_start);
    this.scope.sprint_selected.date_end = get_utc_date(this.scope.sprint_selected.date_end);
    $('#modal_sprint').modal('show');
    return true;
  };

  SprintController.prototype.record_sprint = function() {
    var sprint_selected;
    sprint_selected = angular.copy(this.scope.sprint_selected);
    sprint_selected.date_start = set_utc_date(this.scope.sprint_selected.date_start);
    sprint_selected.date_end = set_utc_date(this.scope.sprint_selected.date_end);
    if (sprint_selected.id) {
      this.Sprint.update(sprint_selected).$promise.then((function(_this) {
        return function(r) {
          _this.get_sprints();
          $('#modal_sprint').modal('hide');
          return true;
        };
      })(this));
    } else {
      this.Sprint.save(sprint_selected).$promise.then((function(_this) {
        return function(r) {
          _this.get_sprints();
          _this.modal_init();
          return true;
        };
      })(this));
    }
    return true;
  };

  SprintController.prototype.delete_sprint = function(sprint) {
    alertify.confirm("Êtes-vous sûr de voiloire supprimer ce sprint?", (function(_this) {
      return function() {
        return _this.Sprint["delete"]({
          id: sprint.id
        }).$promise.then(function(r) {
          _this.get_sprints();
          return true;
        });
      };
    })(this));
    return true;
  };

  return SprintController;

})();

app.controller('SprintController', SprintController);

var ModalTaskController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

ModalTaskController = (function() {
  ModalTaskController.$inject = ['$scope', '$rootScope', 'Task', 'Employee', 'Sprint', '$http', '$q'];

  function ModalTaskController(scope, $rootScope, Task, Employee, Sprint, $http, $q) {
    this.scope = scope;
    this.delete_task = bind(this.delete_task, this);
    this.record_task = bind(this.record_task, this);
    this.update_task = bind(this.update_task, this);
    this.new_task = bind(this.new_task, this);
    this.init = bind(this.init, this);
    this.load_data = bind(this.load_data, this);
    this.load_sprints = bind(this.load_sprints, this);
    this.load_employees = bind(this.load_employees, this);
    this.Task = Task;
    this.Employee = Employee;
    this.Sprint = Sprint;
    this.http = $http;
    this.rootScope = $rootScope;
    this.q = $q;
    this.scope.task = {};
    this.scope.new_task = this.new_task;
    this.scope.update_task = this.update_task;
    this.scope.record_task = this.record_task;
    this.scope.delete_task = this.delete_task;
    $('#modal_task_edit .datetimepicker2').datetimepicker({
      autoclose: true
    });
    this.scope.$on('modal_task', (function(_this) {
      return function(event, task) {
        if (task.id != null) {
          _this.update_task(task);
        } else {
          _this.new_task();
        }
        return true;
      };
    })(this));
    true;
  }

  ModalTaskController.prototype.load_employees = function() {
    var deferred;
    deferred = this.q.defer();
    this.Employee.query().$promise.then((function(_this) {
      return function(r) {
        return deferred.resolve(r.results);
      };
    })(this));
    return deferred.promise;
  };

  ModalTaskController.prototype.load_sprints = function() {
    var deferred;
    deferred = this.q.defer();
    this.Sprint.query().$promise.then((function(_this) {
      return function(r) {
        return deferred.resolve(r.results);
      };
    })(this));
    return deferred.promise;
  };

  ModalTaskController.prototype.load_data = function() {
    var deferred;
    deferred = this.q.defer();
    this.Sprint.query().$promise.then((function(_this) {
      return function(r) {
        return deferred.resolve(r.results);
      };
    })(this));
    return deferred.promise;
  };

  ModalTaskController.prototype.init = function() {
    this.scope.task = {};
    return true;
  };

  ModalTaskController.prototype.new_task = function() {
    this.init();
    this.q.all([this.load_employees(), this.load_sprints()]).then((function(_this) {
      return function(response) {
        _this.scope.employees = response[0];
        _this.scope.sprints = response[1];
        _this.scope.sprints.unshift({
          'name': 'Selectionnez un sprint'
        });
        $('#modal_task_edit').modal('show');
        return true;
      };
    })(this));
    return true;
  };

  ModalTaskController.prototype.update_task = function(task) {
    this.init();
    this.q.all([
      this.Task.get({
        id: task.id
      }).$promise, this.load_employees(), this.load_sprints()
    ]).then((function(_this) {
      return function(response) {
        task = response[0];
        _this.scope.employees = response[1];
        _this.scope.sprints = response[2];
        _this.scope.sprints.unshift({
          'name': 'Selectionnez un sprint'
        });
        _this.scope.task = task;
        _this.scope.task.status = task.status.toString();
        _this.scope.task.date_start = get_utc_datetime(task.date_start);
        _this.scope.task.date_end = get_utc_datetime(task.date_end);
        $('#modal_task_edit').modal('show');
        return true;
      };
    })(this));
    return true;
  };

  ModalTaskController.prototype.record_task = function() {
    var task;
    task = angular.copy(this.scope.task);
    task.date_start = set_utc_datetime(task.date_start);
    task.date_end = set_utc_datetime(task.date_end);
    if (task.date_start === "") {
      delete task.date_start;
    }
    if (task.date_end === "") {
      delete task.date_end;
    }
    if (!task.id) {
      this.Task.save(task).$promise.then((function(_this) {
        return function(r) {
          _this.rootScope.$broadcast("task_recorded", r);
          _this.init();
          return alertify.success("Tâche enregistrée avec succès!");
        };
      })(this), (function(_this) {
        return function(r) {
          alertify.error("Erreur lors de l'enregistrement de la tâche");
          return _this.scope.task.errors = r.data;
        };
      })(this));
    } else {
      this.Task.update(task).$promise.then((function(_this) {
        return function(r) {
          _this.rootScope.$broadcast("task_recorded", r);
          alertify.success("Tâche modifiée avec succès!");
          return $('#modal_sprint').modal('hide');
        };
      })(this), (function(_this) {
        return function(r) {
          alertify.error("Erreur lors de l'enregistrement de la tâche");
          return _this.scope.task.errors = r.data;
        };
      })(this));
    }
    return true;
  };

  ModalTaskController.prototype.delete_task = function(task) {
    alertify.confirm("Supprimer cette tâche?", (function(_this) {
      return function() {
        return _this.Task["delete"](task).$promise.then(function(r) {
          alertify.success("Tâche supprimée avec succès");
          _this.get_tasks();
          return true;
        });
      };
    })(this));
    return true;
  };

  return ModalTaskController;

})();

app.controller('ModalTaskController', ModalTaskController);

console.log('Bonjour')