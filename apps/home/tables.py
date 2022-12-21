import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from apps.home.models import Site, Interface, ApplicationPerInterface, InInterfaceBurst, OutInterfaceBurst
from django_tables2 import A

class SiteTable(tables.Table):
    class Meta:
        model = Site
        template_name = "django_tables2/bootstrap.html"
        fields = ("zonegeo", "site_name", "in_bw", "out_bw", "avg_congestion_in", "avg_congestion_out", "provider",)
        attrs = {'class': 'table table-bordered table-hover table-striped w-100'}

class InterfaceTable(tables.Table):
    class Meta:
        model = Interface
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "deviceName", "deviceIp", "description", "site", )
        attrs = {'class': 'table table-bordered table-hover table-striped w-100'}

class ApplicationPerInterfaceTable(tables.Table):
    if_name = tables.Column(verbose_name='Interface', accessor=A("get_interface_name"))

    class Meta:
        model = ApplicationPerInterface
        template_name = "django_tables2/bootstrap.html"
        fields = ("date", "time", "app_name", "if_name", "router_name", "TxOctets", "TxOctets", "TotalOctets" )
        attrs = {'class': 'table table-bordered table-hover table-striped w-100'}


class InInterfaceBurstTable(tables.Table):
    actions = tables.Column(verbose_name='Get Apps', accessor=A("get_id"))
    if_name = tables.Column(verbose_name='Interface', accessor=A("get_interface_name"))
    router_name = tables.Column(verbose_name='Router', accessor=A("get_router_name"))

    class Meta:
        model = InInterfaceBurst
        template_name = "django_tables2/bootstrap.html"
        fields = ("date", "time", "router_name", "if_name", "InBurst3", "InBurst4" , "applications")
        attrs = {'class': 'table table-bordered table-hover table-striped w-100'}

    def old_render_actions(self, value):
        #url = reverse('comptabilite:updatecomptegeneral', kwargs={'id': value})
        url = "#"
        open = """<a title="Get Apps"  href= {} class="btn btn-sm btn-icon btn-outline-success rounded-circle mr-1">
        <i class="fal fa-pencil"></i></a>""".format(url)
        return format_html(open)

    def old_render_actions(self, value):
        openclose = """<a href="#" data-toggle="modal" data-target="#manageexercice-{}" title="Clôturer Exercice" class="btn btn-sm btn-icon btn-outline-danger rounded-circle mr-1">
                    <i class="fal fa-window-close" style="color:red;"></i></a>""".format(value[0])

        collapse = """
            <!-- app shortcuts -->
              <a href="#" title="Doc Comptable" class="header-icon" data-toggle="dropdown" data-target="#doccomptable">
                <span class="fas fa-cogs"></span>
              </a>
              <div class="dropdown-menu">
                <div class="dropdown-header bg-trans-gradient d-flex justify-content-center align-items-center rounded-top">
                  <h4 class="m-0 text-center color-white">
                    Export Documents Comptables
                    <small class="mb-0 opacity-80">Export Documents Comptables</small>
                  </h4>
                </div>
                <div class="custom-scroll h-100">
                  <ul class="app-list">
                    <li>
                      <a href={} class="app-list-item hover-white">
                        <span class="icon-stack">
                          <i class="base-16 icon-stack-3x color-fusion-500"></i>
                          <i class="base-10 icon-stack-1x color-primary-50 opacity-30"></i>
                          <i class="base-10 icon-stack-1x fs-xl color-primary-50 opacity-20"></i>
                          <i class="fal fa-dot-circle icon-stack-1x text-white opacity-85"></i>
                        </span>
                        <span class="app-list-name">
                          Bilan
                        </span>
                      </a>
                    </li>
                    <li>
                      <a href="#" class="app-list-item hover-white">
                        <span class="icon-stack">
                          <i class="base-7 icon-stack-3x color-info-500"></i>
                          <i class="base-7 icon-stack-2x color-info-700"></i>
                          <i class="ni ni-graph icon-stack-1x text-white"></i>
                        </span>
                        <span class="app-list-name">
                          Resultat
                        </span>
                      </a>
                    </li>
                    <li>
                      <a href="#" class="app-list-item hover-white">
                        <span class="icon-stack">
                          <i class="base-18 icon-stack-3x color-info-700"></i>
                          <span class="position-absolute pos-top pos-left pos-right color-white fs-md mt-2 fw-400">28</span>
                        </span>
                        <span class="app-list-name">
                          Etats Financiers
                        </span>
                      </a>
                    </li>
                    <li>
                      <a href={} class="app-list-item hover-white" data-toggle="modal" data-target="#exportbalance">
                        <span class="icon-stack">
                          <i class="base-7 icon-stack-3x color-info-500"></i>
                          <i class="base-7 icon-stack-2x color-info-700"></i>
                          <i class="fal fa-balance-scale icon-stack-1x text-white"></i>
                        </span>
                        <span class="app-list-name">
                          Balance
                        </span>
                      </a>
                    </li>
                    <li>
                      <a href="#" class="app-list-item hover-white" data-toggle="modal" data-target="#grandlivre">
                        <span class="icon-stack">
                          <i class="base-7 icon-stack-3x color-info-500"></i>
                          <i class="base-7 icon-stack-2x color-info-700"></i>
                          <i class="ni ni-book-open icon-stack-1x text-white"></i>
                        </span>
                        <span class="app-list-name">
                          Grand Livre
                        </span>
                      </a>
                    </li>
                  </ul>
                </div>
              </div>
            <!-- app message -->
        """.format(url_bilancomptable, url_exportbalance)
        return format_html(collapse + openclose)
class OutInterfaceBurstTable(tables.Table):
    if_name = tables.Column(verbose_name='Interface', accessor=A("get_interface_name"))
    router_name = tables.Column(verbose_name='Router', accessor=A("get_router_name"))
    class Meta:
        model = OutInterfaceBurst
        template_name = "django_tables2/bootstrap.html"
        fields = ("date", "time", "router_name", "if_name", "OutBurst3", "OutBurst4", "applications" )
        attrs = {'class': 'table table-bordered table-hover table-striped w-100'}