#### What's new in mod-v1.3-Glass
- Added more glass shaders to match the glass types used in VC.
- Added detection for Blender specific properties that can be generated with the BlenderProps addon (or added manually)
- Changed the add-on icon to the Blender logo

#### What's new in mod-v1.2-Materializer
- Restored video rendering to MP4 (AVI is disabled for now)
- Added material replacement for glass and lasers.
- Added alpha over white background comp for when env is invisible.
- Added Autoshop hdri as standard.
- Added a new EEVEE shadow catcher as default.
- Moved Open in Blender setting to default tab.

#### What's new in mod-v1.1-Blender5 (by andreas.wetter@sejfo.se)
- Made the addon Blender 5.0 compatible (Might still work with 3.6+)
- On import to Blender, animation data on static objects is removed to avoid bloating the file.
- External resources are now packed into the .blend file on export
- Better README formatting

#### What's new 2.3.0:
- added support for the hierarchical dynamic component structures (e.g. PM assembly products)
- support multiple different PM products that are using the same base component with different parameters.
- video output resolution respects now the given resolution (before only the rendering used the resolution but the video file was always fullhd landscape)
- fixing an issue related to missing materials in some layouts with robots (SmartMaterial related issue)
- improved transparent material handling
- added SimplifiedTransparent mode to support rendering transparent objects inside other transparent objects
- animation recording start and end time don't keep resetting to 0 and 5
- added new default floor textures
- added new default LightPresets
- exposure and lighting defaults tweaked 
- control the backdrop color when Env map is set to not visible (use image or ColorRGB setting)
- blenderer addon version number not showing in the ui anymore
- animation frame index calculated based on the time stamp to ensure correct animation sync

