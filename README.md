globlocks
=========

Block/Widget library to make your Wagtail site more complete

## TODO

* Documentation
* Tests
* (blocks) components/images
* (blocks) components/menus
* (templates) components/menus

## Implemented

* blocks with settings
* toggleable-visibility blocks
* richtext alignment (with headers and inline entities)
* color picker widget/block/panel/(model)field
* range slider widget/block
* justify text alignment widget/block (targets specified inputs; aligns them in admin)
* toolbar widget/block; a richtext toolbar for your regular inputs
* fontpicker widget
* components
  * images (NYI)
  * menus (NYI)
  * headers
  * text
  * image/text

Quick start
-----------

1. Add 'globlocks' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
       ...,
       'globlocks',
       'conditional_field',
   ]
   ```
2. ...

## Richtext Alignment

`globlocks` has a richtext feature for text alignment; without the limits that feature would normally impose.

*Normally* - headings would not be able to get aligned. **This is a problem.**

Luckily, we have the solution! *And you can use it too!*

**To add the alignment features to your richtext**

1. Follow the installation steps for `globlocks`.
2. Add `text-alignment` to your richtext features. (it is included in default features)

To align it on the frontend too; add the following CSS:

```css
.text-left {
    text-align: left;
}
.text-center{
    text-align: center;
}
.text-right {
    text-align: right;
}
```
