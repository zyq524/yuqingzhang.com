$(function () {
    var Project = Backbone.Model.extend({
        defaults: {
            name: '',
            url: '',
            description: ''
        }
    });

    var ProjectList = Backbone.Collection.extend({
        model: Project,
        sync: function (method, model, options) {
            var params = _.extend({
                type: 'GET',
                dataType: 'jsonp',
                url: model.url(),
                jsonpCallback: 'projects'
            }, options);

            return $.ajax(params);
        },
        parse: function (response) {
            return response;
        },
        url: function () {
            return 'http://zhangyuqinglabs.blob.core.windows.net/qswareportal/projects.json';
        }
    });

    var ProjectView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#project-template').html()),
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        clear: function () {
            this.model.clear();
        }
    });

    var Projects = new ProjectList;

    var ProjectsView = Backbone.View.extend({
        el: $("#main"),

        initialize: function () {
            Projects.bind('reset', this.addAll, this);

            Projects.fetch();
        },

        addOne: function (project) {
            var view = new ProjectView({ model: project });
            this.$("#projects").append(view.render().el);
        },
        addAll: function () {
            Projects.each(this.addOne);
        }
    });

    var App = new ProjectsView;
});