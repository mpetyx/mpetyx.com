MapEntity.TogglableFilter = L.Class.extend({
    includes: L.Mixin.Events,
    options: {},

    initialize: function () {
        this.button = '#filters-btn';

        this.fields = {};
        this.visible = false;
        this.popover = $('#filters-popover')
                          .popover({
                              placement: 'bottom',
                              html: true,
                              content: '',
                              title: 'Useless'
                          });
        this.hover = $('#filters-hover')
                          .popover({
                              placement: 'bottom',
                              html: true,
                              content: this.infos.bind(this),
                              title: tr("Current criteria")
                          });

        $(this.button).click(this.toggle.bind(this));
        $(this.button).hover(this.showinfo.bind(this));
        var self = this;
        $('#mainfilter').find('select,input').change(function (e) {
            self.setfield(this);
        });

        // Move all topology-filters to separate tab
        $('#mainfilter .topology-filter').parent('p')
                                         .detach().appendTo('#mainfilter > .right');

        // Use chosen for multiple values
        // Remove empty value (set with empty_label in Django for all choice fields)
        $('#mainfilter select[multiple] option:first-child').remove();
        $("form#mainfilter").bind("reset", function() {
            setTimeout(function() {
                $('form#mainfilter select[multiple]').trigger('liszt:updated');
            }, 1);
        });
        // Make sure filter-set class is added if a choice is selected.
        $('#mainfilter select[multiple]').chosen().on('change', function (e) {
            var $target = $(e.target),
                name = $target.attr('name'),
                $container = $('div#id_' + name + '_chzn > ul');
            if ($(e.target).find('option:selected').length > 0) {
                $container.addClass('filter-set');
            }
            else {
                $container.removeClass('filter-set');
            }
        });
    },

    tip: function () {
        return this.popover.data('popover').$tip;
    },

    htip: function () {
        return this.hover.data('popover').$tip;
    },

    __reposition: function (tip) {
        // Adjust position nicely along filter button
        var btnleft = $(this.button).position().left,
            btnwidth = $(this.button).width();
        tip.css('left', btnleft + btnwidth/2 - tip.width()/2);
    },

    showinfo: function () {
        // If popover is already visible, do not show hover
        if (this.visible)
            return;
        this.hover.popover('toggle');
        // Adjust popover width
        this.htip()
            .width(this.htip().find('.popover-title').outerWidth());
        this.__reposition(this.htip());
    },

    infos: function () {
        if (Object.keys(this.fields).length === 0)
            return "<p>" + tr("No filter") + "</p>";
        // We do not use handlebars just for this. If more to come, we will !
        var p = '<p><span class="filter-info">%name%</span>: %value%</p>';
        var i = '';
        for (var k in this.fields) {
            var f = this.fields[k];
            i += p.replace('%name%', f.label).replace('%value%', f.value);
        }
        return i;
    },

    toggle: function () {
        /* Show/Hide popover */
        if (this.visible) {
            // The whole $tip will be deleted, save the panel
            // and add it to the DOM so the dynamic filters still works.
            $('#filters-wrapper').append(
                this.tip().find('#filters-panel').detach()
            );
        }

        this.popover.popover('toggle');
        this.visible = !this.visible;

        if (this.visible) {
            this.tip()
              .empty()
              .append('<div class="arrow"/>')
              .append($('#filters-wrapper #filters-panel').detach());

            // Adjust popover width
            this.tip()
                .width(this.tip().find('#filters-panel form').outerWidth());

            this.__reposition(this.tip());
        }
    },

    setfield: function (field) {
        var label = $(field).data('label'),
            name = $(field).attr('name'),
            val = $(field).val(),
            set = val !== '' && val != [''];

        // Consider a value set if it is not the first option selected
        if ($(field).is('select[multiple]')) {
            set = val !== null;
        }
        else if ($(field).is('select')) {
            set = val != $(field).find('option').first().val();
        }

        // Displayed value
        var value = val;
        if (field.tagName == 'SELECT') {
            value = $(field).find("option:selected").text();
        }

        if (set) {
            this.fields[name] = {name: name, val:val, value:value, label:label};
        }
        else {
            delete this.fields[name];
        }

        if (set) {
            $(field).addClass('filter-set');
        }
        else {
            $(field).removeClass('filter-set');
        }
        return set;
    },

    setsubmit: function () {
        this.submitted = true;
        // Show fields as bold
        // Show button as active
        if (Object.keys(this.fields).length === 0) {
            $('#filters-btn').addClass('btn-info');
            $('#filters-btn').removeClass('btn-warning');
        }
        else {
            $('#filters-btn').removeClass('btn-info');
            $('#filters-btn').addClass('btn-warning');
        }
    }
});
