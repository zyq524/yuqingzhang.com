$(function () {
    var Albumn = Backbone.Model.extend({
        defaults: {
            albumnUrl: '',
            title: '',
            thumbImg: '',
            comment: ''
        }
    });

    var AlbumnList = Backbone.Collection.extend({
        model: Albumn,
        sync: function (method, model, options) {
            var params = _.extend({
                type: 'GET',
                dataType: 'jsonp',
                url: model.url(),
                jsonpCallback: 'albumns'
            }, options);

            return $.ajax(params);
        },
        parse: function (response) {
            return response;
        },
        url: function () {
            return 'http://zhangyuqinglabs.blob.core.windows.net/qswareportal/gallery.json';
        }
    });

    var AlbumnView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('#albumn-template').html()),
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        clear: function () {
            this.model.clear();
        }
    });

    var Albumns = new AlbumnList;

    var AlbumnsView = Backbone.View.extend({
        el: $("#main"),

        initialize: function () {
            Albumns.bind('reset', this.addAll, this);

            Albumns.fetch();
        },

        addOne: function (albumn) {
            var view = new AlbumnView({ model: albumn });
            this.$("#albumns").append(view.render().el);
        },
        addAll: function () {
            Albumns.each(this.addOne);
        }
    });

    var App = new AlbumnsView;
});