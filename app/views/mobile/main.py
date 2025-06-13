from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager
from app.viewmodels.product_viewmodel import ProductViewModel

class ProductListScreen(MDScreen):
    def __init__(self, view_model: ProductViewModel, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_label = MDLabel(
            text="Products",
            halign="center",
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.title_label)

        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.error_label)

        scroll = ScrollView()
        self.products_list = MDList()
        scroll.add_widget(self.products_list)
        layout.add_widget(scroll)

        self.add_widget(layout)

        self.view_model.load_products()
        self.update_products_list()

    def update_products_list(self):
        self.products_list.clear_widgets()
        if self.view_model.error_message:
            self.error_label.text = self.view_model.error_message
        else:
            self.error_label.text = ""
            for product in self.view_model.products:
                item = TwoLineListItem(
                    text=product.name,
                    secondary_text=f"Price: ${product.price:.2f}",
                    on_release=lambda x, p=product: self.show_product_details(p)
                )
                self.products_list.add_widget(item)

    def show_product_details(self, product):
        self.view_model.select_product(product.id)
        self.manager.current = 'product_details'

class ProductDetailsScreen(MDScreen):
    def __init__(self, view_model: ProductViewModel, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.back_button = MDRaisedButton(
            text="Back to List",
            pos_hint={'center_x': .5},
            on_release=self.go_back
        )
        layout.add_widget(self.back_button)

        self.details_card = MDCard(
            orientation='vertical',
            padding=15,
            spacing=10,
            size_hint=(None, None),
            size=("300dp", "400dp"),
            pos_hint={"center_x": .5, "center_y": .5}
        )

        self.name_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Primary"
        )
        self.details_card.add_widget(self.name_label)

        self.price_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.price_label)

        self.stock_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.stock_label)

        self.reserved_label = MDLabel(
            text="",
            halign="center"
        )
        self.details_card.add_widget(self.reserved_label)

        layout.add_widget(self.details_card)
        self.add_widget(layout)

    def on_enter(self):
        if self.view_model.selected_product:
            product = self.view_model.selected_product
            self.name_label.text = product.name
            self.price_label.text = f"Price: ${product.price:.2f}"
            self.stock_label.text = f"Stock: {product.stock}"
            self.reserved_label.text = f"Reserved: {product.reserved}"

    def go_back(self, *args):
        self.manager.current = 'product_list'

class CrossPlatformApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        view_model = ProductViewModel()

        product_list = ProductListScreen(view_model, name='product_list')
        product_details = ProductDetailsScreen(view_model, name='product_details')

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(product_list)
        self.screen_manager.add_widget(product_details)
        self.screen_manager.current = 'product_list'

        return self.screen_manager

if __name__ == '__main__':
    CrossPlatformApp().run() 
